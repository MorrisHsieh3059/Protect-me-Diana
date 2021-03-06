##################################
#########   Just Import  ##########
##################################

from __future__ import unicode_literals
import errno
import os
import sys
import tempfile
from argparse import ArgumentParser
from flask import Flask, request, abort, jsonify, send_from_directory

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import LineBotApiError, InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    TemplateSendMessage, CarouselTemplate, PostbackEvent,
    StickerMessage, StickerSendMessage, ImagemapSendMessage,
    ImageMessage, ImageSendMessage
)

from questionnaire.extract_function import extract, revise_extract       #RE抓數字
from questionnaire.ct_push import ct_push               #抓推播新的carousel template
from questionnaire.confirm import confirm          #抓confirm template 進來
from questionnaire.carousel import *               #抓caousel columns
from questionnaire.confirm_push import confirm_push
from questionnaire.next import next
from questionnaire.imgmap_push import floor_plan
from questionnaire.tempview import takeFirst, tempview, tempview_confirm, cat_tempview, cat_tempview_confirm
from questionnaire.converter import converter
from questionnaire.revise import revise_idiot, revise_confirm, revise_able, cat_revise_confirm
from questionnaire.image_upload import Image_Upload

from account.account_confirm import account_confirm
from account.get_account_db import (
    get_account_db, get_userid_db, delete_userid_db,
    get_school_db, no_repeat_school_db, get_county_db
)

from connect.fetch import fetch
from connect.detail import detail
from connect.event import event
from connect.building import building
from connect.overall import overall

from db.database import Database

from chat_module.Data import Data

from liangyuan.func import *

DB = Database(os.environ.get('DATABASE_URL'), db_type='postgres')
# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')
app.config['JSON_AS_ASCII'] = False

    ##################################
    #########儲存使用者填答紀錄#########
    ##################################

data = Data()
account = {} #帳號設定問問題用的
account_q = 0 #記住帳號設定的題數

    ##################################
    ##########  Good Simu   ##########
    ##################################

line_bot_api = None
if os.environ.get("FLASK_ENV") == "development":
    line_bot_api = LineBotApi(os.environ.get("TOKEN"), "http://localhost:8080")
else:
    line_bot_api = LineBotApi(os.environ.get("TOKEN"))

handler = WebhookHandler(os.environ.get("SECRET"))

@app.route('/report/<path:name>')
# 檔案在不在,在哪裡/有沒有亂戳,怎麼丟
def reportroute(name):
    name = 'index.html' if name is "" else name
    path = os.path.join("report", name)
    with open(path, encoding="utf-8") as f:
        content = f.read()
    return content

def send_js(name):
    return send_from_directory('js', name)

@app.route('/overall')
def overallroute():
    assessment_id = request.args.get('assessment_id')
    return jsonify(overall('{"assessment_id":' + assessment_id + '}', DB))

@app.route('/event')
def eventroute():
    return jsonify(event(DB))

@app.route('/fetch')
def fetchroute():
    county = request.args.get('county')
    ass_id  = request.args.get('assessment_id')
    return jsonify(fetch('{"county":"' + county + '", "assessment_id":' + ass_id + '}', DB))

@app.route('/building')
def buildingroute():
    school_id = request.args.get('school_id')
    ass_id = request.args.get('assessment_id')
    return jsonify(building('{"school_id":"%s","assessment_id":%s}' % (school_id, ass_id), DB))

@app.route('/detail')
def detailroute():
    # userid = request.args.get('userid')
    ass_id = request.args.get('assessment_id')
    building_id = request.args.get('building_id')
    # return jsonify(detail('{"userid":"%s","assessment_id":"%s","building_id":"%s"}' % (userid, ass_id, building_id), DB))
    return jsonify(detail('{"assessment_id":"%s","building_id":"%s"}' % (ass_id, building_id), DB))

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        print("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            print("  %s: %s" % (m.property, m.message))
        print("\n")
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    userid = event.source.user_id
    user_data = data.get_user(userid)
    print(f"\n\n\n{user_data}\n\n\n")

    """
        Other msg
    """
    if text == '我要設定帳號':
            ret = [
                TextSendMessage(text="此功能暫時關閉。"),
                StickerSendMessage(package_id=11537,sticker_id=52002770),
            ]

            line_bot_api.reply_message(event.reply_token, ret)

    elif text == '請給我使用須知':
        ret1 = TextSendMessage(text="歡迎使用本平台😁\n本平台是作為學校校安機關的安全檢核系統\n目前功能僅有表單檢核功能")
        ret2 = TextSendMessage(text="【填寫表單須知】：\n您可以透過點選選單中的問卷按鈕，或是輸入「問卷」來呼叫問卷。\n本問卷提供兩種填答方式：\n\n1.快速檢核：若情況緊急，請使用此捷徑\n2.常規問卷：共分成四類選單，可交叉填答\n【注意】：兩種填寫方式不可交叉填寫")
        ret3 = TextSendMessage(text="本次填寫的事件為：" + str(DB.get_latest_assessment_id_db()[1]))
        line_bot_api.reply_message(
            event.reply_token, [ret1] + [ret2] + [ret3])


    elif text == '我要統計資料' or text == 'I need the summary of inspection results.':
        ret = TextSendMessage(text="https://pmdiana.hcilab.katrina.tw/report/index.html")
        line_bot_api.reply_message(event.reply_token, ret)

    """
        Questionnaire Process
    """
    if userid not in data.get_all_users() and userid not in DB.get_yitianda_db():
        data.add_user(userid)
        print("新用戶!")

    if userid in DB.get_yitianda_db():
        ret1 = TextSendMessage(text="您已為本次事件提供災情回覆咯~")
        ret2 = TextSendMessage(text="本次填寫的事件為：" + str(DB.get_latest_assessment_id_db()[1]))
        line_bot_api.reply_message(
            event.reply_token, [ret1] + [ret2])

    else:
        ### Module 1 ###
        if data.get_user_status(userid) == "pre":
            print("第一模組")
            signal = toCheck(event, line_bot_api)
            data.set_user_status(userid, signal[0])
            if signal[1] != "": # Record building name
                # building_id = DB.get_building_id(signal[1])
                # print(building_id)
                data.set_user_building(userid, signal[1]) # 紀錄建築名字

        ### Module 2 ###
        elif data.get_user_status(userid) == "pre-class": # module 1 跟 2 的街口
            if data.get_user_current(userid) == (): # 第一次填寫的時候
                line_bot_api.unlink_rich_menu_from_user(userid)
                ct_container = ct_push(data.get_all_users(), userid, 0, 0, DB) # 前面ㄉ0代表推出【快速/標準carousel】
                                                               # 後面ㄉ0代表非(類別不修改)
                carousel_template = CarouselTemplate(columns=ct_container)
                template_message = TemplateSendMessage(alt_text='災情回覆問卷', template=carousel_template)
                line_bot_api.reply_message(event.reply_token, template_message)
                data.set_user_status(userid, "00")
                data.set_user_building(userid, text) # 紀錄教室名字

            elif user_data['Answered']['Quick'] != []: #選擇快速檢核後，阻止其跳回標準檢核
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text="您已選擇快速檢核！請填頁面上的最後一題"))

            else:
                ct_container = ct_push(data.get_all_users(), userid, 1, 0, DB) #1代表推出【四大題組carousel】
                carousel_template = CarouselTemplate(columns=ct_container)
                template_message = TemplateSendMessage(alt_text='問卷選單', template=carousel_template)
                line_bot_api.reply_message(event.reply_token, template_message)

        elif user_data["status"] == "01" and "題已回覆" not in text:
            #首次填答問卷選擇【待改進】
            print('進入【首次填答待改進】')
            cat, Q = user_data["current"]
            ret = None

            data.add_user_answered(userid, cat, Q)
            _ = data.get_user_current(userid) + (text,)
            data.set_user_current(userid, _)
            data.add_user_feedback(userid, (cat, Q, text))

            ## 請使用者點選問題所在位置
            floor = floor_plan()
            line_bot_api.reply_message(
                event.reply_token, [TextSendMessage(text='『' + text + '』已收到回覆')] + [TextSendMessage(text="請點選問題所在位置(九宮格)")] + [floor])

            data.set_user_status(userid, "02") # 等待使用者戳點

        # 使用者要戳 平面圖
        elif user_data["status"] == "02":
            if text in ['上左', '上中', '上右', '中左', '中中', '中右', '下左', '下中', '下右']:
                data.set_user_spec_feedback_pos(userid, text)
                _ = data.get_user_current(userid) + (text,)
                data.set_user_current(userid, _)
                print(f"\n\n--\n{event}\n\--n\n\n")

                data.set_user_status(userid, "03") # 等他傳照片
                line_bot_api.reply_message(
                    event.reply_token, [TextSendMessage(text="請傳照片，並稍後照片上傳時間(約數秒)🙏")])
            else:
                line_bot_api.reply_message(event.reply_token, [TextSendMessage(text="請點選上方平面圖！")])

        #類別/最終修改答案，告訴系統要改的題目(EG, C8)
        elif user_data["status"] in ["10", "20"] and "題已回覆" not in text:
            try:
                if revise_able(revise_extract(text)[0], revise_extract(text)[1]) is True:
                    cat = revise_extract(text)[0]
                    i   = revise_extract(text)[1]#相對題號

                    # 禁止跨類別條件：       同類別        or          最終檢查
                    if cat == user_data["current"][0] or user_data["status"] == "20":
                        data.set_user_current(userid, (cat, i))
                        data.del_user_answered(userid, cat, i)

                        newlist = []
                        for j in range(len(user_data["feedback"])):#從feedback拿掉要改的題的資料
                            if not(cat == user_data["feedback"][j][0] and i == user_data["feedback"][j][1]) :
                                newlist.append(user_data["feedback"][j])
                        data.set_user_feedback(userid, newlist)

                        #丟confirm
                        if user_data["status"] == "10":   #各類別要改答案
                            print('\n進入【類別修改答案】')
                            ret = [cat_revise_confirm(cat, i, DB)]

                        elif user_data["status"] == "20":   # 最終要改答案
                            print('\n進入【最終修改答案】')
                            ret = [revise_confirm(cat, i, DB)]

                        data.add_user_answered(userid, cat, i)

                    else:
                        ret = TextSendMessage(text="請修改當前類別：%s." % user_data["current"][0])

                    line_bot_api.reply_message(event.reply_token, ret)

                else:
                    ret = revise_idiot(text, revise_extract(text)[0], revise_extract(text)[1])
                    line_bot_api.reply_message(
                        event.reply_token, TextSendMessage(text=ret))
            except:
                print("類別修改 題號判斷 失敗了喔喔喔喔喔喔喔")

        # 處理類別/最終改答案的時候，輸入的待改進的內容(EG, 哈囉MO)
        elif user_data["status"] in ["11", "21"] and "題已回覆" not in text:
            cat, Q = user_data["current"]
            data.add_user_feedback(userid, (cat, Q, text, "N/A", "N/A"))
            data.add_user_answered(userid, cat, Q)
            output = data.get_user_feedback(userid)

            if user_data["status"] == "21": #最終修改答案選待改進，revise_result會是false
                print('進入【最終修改待改進】')
                data.set_user_status(userid, "20")
                ret = tempview_confirm(output, DB)

            elif user_data["status"] == "11": #類別修改答案選待改進，cat_revise_result會是false
                print('進入【類別修改待改進】')
                data.set_user_status(userid, "10")
                ret = cat_tempview_confirm(cat, output, DB)

            line_bot_api.reply_message(
                event.reply_token, [TextSendMessage(text='『' + text + '』已收到回覆')] + ret)

    ##################################
    ##########Postback Event#########
    ##################################

@handler.add(PostbackEvent)
def handle_postback(event):
    userid = event.source.user_id #取得Userid
    user_data = data.get_user(userid)

    global account
    global account_q

    ##################################
    ########## 填問卷的過程 ###########
    ##################################

    #QC丟問題，相對題號
    if event.postback.data == 'Quick':
        line_bot_api.reply_message(
            event.reply_token, confirm_push(data.get_all_users(), userid, event.postback.data, DB))

    elif event.postback.data == 'Standard':
        ct_container = ct_push(data.get_all_users(), userid, 1, 0, DB)  #把4類別加進來
        carousel_template = CarouselTemplate(columns=ct_container)
        template_message = TemplateSendMessage(alt_text='詳細災情回覆問卷', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    #四類丟問題，相對題號
    elif event.postback.data in ['Normal', 'Indoors', 'Corridor', 'Outdoors']:
        line_bot_api.reply_message(
            event.reply_token, confirm_push(data.get_all_users(), userid, event.postback.data, DB))

    #戳題目的confirm template的時候
    try:
        parse = extract(event.postback.data) #[0]是類別；[1]是相對題號；[2]是沒問題/待改進
        cat, Q, ans = parse
        data.set_user_current(userid, (cat, Q))
        ret = None
        last = len(DB.get_category(cat))

        #處理carousel template
        #填完該類別最後一題且最後一題是沒問題
        if Q == last and ans == 'OK':
            data.set_user_status(userid, "00")
            data.add_user_answered(userid, cat, Q)
            output = data.get_user_feedback(userid)

            print('進入【(第一次)類別TEMPVIEW】')
            print(f"\n\n====\ncat: |{cat}\nOutput: |{output}\n")
            ret = cat_tempview_confirm(cat, output, DB)#推第一次類別修改tempview confirm template
            ct_container = ct_push(data.get_all_users(), userid, 1, 0, DB)

            #QC填完
            if cat == "Quick" and Q == last:
                print('進入【最終TEMPVIEW】──QC的路，不要怕上一句話，因為她是必經之路')
                output = data.get_user_feedback(userid)
                ret = tempview_confirm(output, DB)#推第一次最終修改tempview confirm template

        #處理題目的confirm template
        #待改進的話，或是非該類別的最後一題
        else:
            ret, _ = next(data.get_all_users(), userid, parse, DB)
            data.set_user_status(userid, _)

        line_bot_api.reply_message(event.reply_token, ret)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('ERROR:', exc_type, exc_obj, fname, exc_tb.tb_lineno)
        print(event.postback.data)

        if event.postback.data == 'edit=NO':
            data.set_user_status(userid, "00")
            output = data.get_user_feedback(userid)
            build, room = data.get_user_building(userid)
            for feed in range(len(output)):
                output[feed] += (build,)
                output[feed] += (room,)

            DB.get_feedback(output, userid, data.get_user_building(userid)[0]) #寫進資料庫
            print('進入【最終修改答案不修改】，結束問卷')
            print(f"\n========================\nThis is feedback:\n{output}\n========================\n")

            ret = [
                TextSendMessage(text="已收到您的回覆～謝謝您的貢獻！"),
                StickerSendMessage(package_id=11537,sticker_id=52002739),
            ]
            line_bot_api.reply_message(event.reply_token, ret)

            data.remove_user(userid)

        if event.postback.data == 'edit=OK':
            print('進入【最終修改答案要修改】，要求輸入修改題號')
            data.set_user_status(userid, "20")
            ret = [
                TextSendMessage(text="請問您要修改哪一題呢?"),
                TextSendMessage(text="【注意】：當您填寫快速檢核時，不能修改其他四類問題；反之亦然。"),
                TextSendMessage(text="請按照下列格式填寫：\n一般檢查(Normal)簡寫為N\n室內(Indoors)簡寫為I\n走廊(Corridor)簡寫為C\n室外(Outdoors)簡寫為O\n再加上題號，例如：\nN7(一般檢查的第七題)"),
            ]
            line_bot_api.reply_message(event.reply_token, ret)

        if event.postback.data == 'cat_edit=NO':
            print('進入【類別修改答案不修改】，丟出類別選單')
            ct_container = ct_push(data.get_all_users(), userid, 1, 1, DB)
            if ct_container == "All cats have already checked!": # 類別全部修改過後，進入最終環節
                print('進入【最終TEMPVIEW】──標準填完了唷，不要怕上一句話，因為她是必經之路')
                output = data.get_user_feedback(userid)
                ret = tempview_confirm(output, DB)
            else:
                carousel_template = CarouselTemplate(columns=ct_container)
                ret = TemplateSendMessage(alt_text='問卷選單', template=carousel_template)

            line_bot_api.reply_message(event.reply_token, ret)

        if 'cat_edit=OK' in event.postback.data:
            print('進入【類別修改答案要修改】，要求輸入修改題號')
            data.set_user_status(userid, "10")

            ## 避免戳 Normal1, Indoors1, Corridor1, Outdoors1 的時候類別被鎖住
            cate = str(event.postback.data).split(';')[1] if ';' in event.postback.data else ''
            print('\n===<%s>===\n' % cate)
            relq = user_data["current"][1]
            _ = (cate, relq) if cate != '' else user_data["current"]
            data.set_user_current(userid, _)
            ret = [
                TextSendMessage(text="請問您要修改哪一題呢?"),
                TextSendMessage(text="【注意】：只能修改當前題組，欲修改其他題組，請於所有問題答畢後修改"),
                TextSendMessage(text="請按照下列格式填寫：\n一般檢查(Normal)簡寫為N\n室內(Indoors)簡寫為I\n走廊(Corridor)簡寫為C\n室外(Outdoors)簡寫為O\n再加上題號，例如：\nN7(一般檢查的第七題)"),
            ]
            line_bot_api.reply_message(event.reply_token, ret)

    ##################################
    ####### 類別修改答案的過程 #########
    ##################################

    if 'cat_revise=' in event.postback.data and 'OK' in event.postback.data:#沒問題
        print('進入【類別修改答案沒問題】，丟出cat_tempview')
        output = data.get_user_feedback(userid)
        ret = cat_tempview_confirm(user_data["current"][0], output, DB)#把它目前的回答推個confirm template給他看看
        line_bot_api.reply_message(event.reply_token, ret)

    elif 'cat_revise=' in event.postback.data and 'NO' in event.postback.data:#待改進
        print('進入【類別修改答案待改進】，請簡述災情')
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="請簡述災情"))
        data.set_user_status(userid, "11")

    ##################################
    ####### 最終修改答案的過程 #########
    ##################################

    if 'all_revise=' in event.postback.data and 'OK' in event.postback.data:#沒問題
        print('進入【最後修改答案沒問題】，丟出tempview')
        output = data.get_user_feedback(userid)
        ret = tempview_confirm(output, DB)#把它目前的回答推個confirm template給他看看
        line_bot_api.reply_message(event.reply_token, ret)

    elif 'all_revise=' in event.postback.data and 'NO' in event.postback.data:#待改進
        print('進入【最後修改答案待改進】，請簡述災情')
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="請簡述災情"))
        data.set_user_status(userid, "21")

    ##################################
    ########## 重設帳號或不設 #########
    ##################################

    if event.postback.data == 'account_reset':
        delete_userid_db(userid, DB)
        account[userid] = {'userid':userid, 'name':0, 'county':0, 'school':0, 'phone':0}
        ret = TextSendMessage(text="請問您尊姓大名？")
        line_bot_api.reply_message(event.reply_token, ret)
        account_q = 1

    elif event.postback.data == 'account_remain':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="好的，謝謝😁"))

    #######################################
    ########## ImageMessage Event #########
    #######################################

@handler.add(MessageEvent, message=ImageMessage)
def handle_content_message(event):
    userid = event.source.user_id
    img_id = event.message.id
    user_data = data.get_user(userid)

    if user_data["status"] == "03": # 首次待改進的照片輸入
        """ Part 1: imgur儲存照片加到 feedback 後面 """
        file_path = './temp.jpg'
        # download img to local
        message_content = line_bot_api.get_message_content(img_id)
        with open(file_path, 'wb') as fd:
            for chunk in message_content.iter_content():
                fd.write(chunk)
        # upload local img to 'imgur'
        img = Image_Upload(file_path)
        url = img.upload_photo()
        data.set_user_spec_feedback_img(userid, url)

        print(f"\n*****************This is feedback:\n{data.get_user_feedback(userid)}\n*****************\n")
        # delete local img
        os.remove(file_path)

        """ Part 2: 下一提 或是 類別檢核 """
        data.set_user_status(userid, "00")
        cat, Q, _, _ = data.get_user_current(userid)
        last = len(DB.get_category(cat))

        if Q == last:
            output = data.get_user_feedback(userid)
            print('進入【(第一次)類別TEMPVIEW】──待改進的路')
            ret = cat_tempview_confirm(cat, output, DB)#推第一次類別修改tempview confirm template
            data.set_user_status(userid, "10")

            # QC
            if cat == "Quick" and Q == last: # or ct_container == [Normal1, Indoors1, Corridor1, Outdoors1]:
                output = data.get_user_feedback(userid)
                ret = tempview_confirm(output, DB)

        else:
            ret = [confirm(cat, Q, DB)]

        line_bot_api.reply_message(
            event.reply_token, [TextSendMessage(text='收到照片了！請繼續下一題 👌')] + ret)
