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
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    TemplateSendMessage, CarouselTemplate, PostbackEvent,
    StickerMessage, StickerSendMessage,
)

from questionnaire.extract_function import extract, revise_extract       #RE抓數字
from questionnaire.ct_push import ct_push               #抓推播新的carousel template
from questionnaire.confirm import confirm          #抓confirm template 進來
from questionnaire.carousel import *               #抓caousel columns
from questionnaire.confirm_push import confirm_push
from questionnaire.next import next
from questionnaire.get_res_db import get_feedback
from questionnaire.get_question_db import get_category
from account.get_account_db import (
    get_account_db, get_userid_db, delete_userid_db,
    get_school_db, no_repeat_school_db, get_county_db
)
from account.account_confirm import account_confirm
from questionnaire.tempview import takeFirst, tempview, tempview_confirm, cat_tempview, cat_tempview_confirm
from questionnaire.converter import converter
from questionnaire.revise import revise_idiot, revise_confirm, revise_able, cat_revise_confirm
from questionnaire.get_yitianda_db import get_yitianda_db
from connect.fetch import fetch
from connect.detail import detail
from connect.event import event
from assessment.get_latest_assessment_id_db import get_latest_assessment_id_db

from db.database import Database

from werkzeug.contrib.cache import SimpleCache, MemcachedCache


db = Database(os.environ.get('DATABASE_URL'), db_type='postgres')
# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')

app.config['JSON_AS_ASCII'] = False

    ##################################
    #########儲存使用者填答紀錄#########
    ##################################

data = {}
account = {} #帳號設定問問題用的
account_q = 0 #記住帳號設定的題數

    ##################################
    ##########  Good Simu   ##########
    ##################################

cache = None
line_bot_api = None

if os.environ.get("FLASK_ENV") == "development":
    line_bot_api = LineBotApi(os.environ.get("TOKEN"), "http://localhost:8080")
    # cache = SimpleCache()

#區分成本機用的跟遠端server用的資料庫
#EX:本機是MYSQL 雲端是POSTGRE
else:
    line_bot_api = LineBotApi(os.environ.get("TOKEN"))
    # cache = MemcachedCache([os.environ.get("CACHE_URL")])

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

@app.route('/event')
def eventroute():
    return jsonify(event(db))

@app.route('/fetch')
def fetchroute():
    county = request.args.get('county')
    ass_id  = request.args.get('assessment_id')
    return jsonify(fetch('{"county":"' + county + '", "assessment_id":' + ass_id + '}', db))

@app.route('/detail')
def detailroute():
    userid = request.args.get('userid')
    ass_id = request.args.get('assessment_id')
    return jsonify(detail('{"userid":"' + userid + '", "assessment_id":' + ass_id + '}', db))

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


    if text == '請給我使用須知':
        ret1 = TextSendMessage(text="歡迎使用本平台😁\n本平台是作為學校校安機關的安全檢核系統\n目前功能僅有表單檢核功能")
        ret2 = TextSendMessage(text="【填寫表單須知】：\n您可以透過點選選單中的問卷按鈕，或是輸入「問卷」來呼叫問卷。\n本問卷提供兩種填答方式：\n\n1.快速檢核：若情況緊急，請使用此捷徑\n2.常規問卷：共分成四類選單，可交叉填答\n【注意】：兩種填寫方式不可交叉填寫")
        ret3 = TextSendMessage(text="本次填寫的事件為："+str(get_latest_assessment_id_db(db)[1]))
        line_bot_api.reply_message(
            event.reply_token, [ret1] + [ret2] + [ret3])


    if text == '我要統計資料' or text == 'I need the summary of inspection results.':
        ret = TextSendMessage(text="https://pmdiana.hcilab.katrina.tw/report/index.html")
        line_bot_api.reply_message(event.reply_token, ret)

    if text == '請給我表單填寫' or text == 'I need the questionnaire.':

        if userid not in get_yitianda_db(get_latest_assessment_id_db(db)[0], db): #確認是否填答過最新事件的問卷
            if userid not in data: #沒有USERID的話，add key(第一次填寫的時候)
                data[userid] = {
                                  "Answered":
                                      {
                                        "Quick": [],
                                        "Normal":[],
                                        "Indoors":[],
                                        "Corridor":[],
                                        "Outdoors":[]
                                      },
                                  "status": "00",
                                  "feedback": [],
                                  "current": (),
                               }

                ct_container = ct_push(data, userid, 0, 0, db) # 前面ㄉ0代表推出【快速/標準carousel】
                                                           # 後面ㄉ0代表非(類別不修改)
                carousel_template = CarouselTemplate(columns=ct_container)
                template_message = TemplateSendMessage(alt_text='災情回覆問卷', template=carousel_template)
                line_bot_api.reply_message(event.reply_token, template_message)

            elif data[userid]['Answered']['Quick'] != []: #選擇快速檢核後，阻止其跳回標準檢核
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text="您已選擇快速檢核！請填頁面上的最後一題"))

            else:
                ct_container = ct_push(data, userid, 1, 0, db) #1代表推出【四大題組carousel】
                carousel_template = CarouselTemplate(columns=ct_container)
                template_message = TemplateSendMessage(alt_text='問卷選單', template=carousel_template)
                line_bot_api.reply_message(event.reply_token, template_message)

        else:
            ret1 = TextSendMessage(text="您已為本次事件提供災情回覆咯~")
            ret2 = TextSendMessage(text="本次填寫的事件為："+str(get_latest_assessment_id_db(db)[1]))
            line_bot_api.reply_message(
                event.reply_token, [ret1] + [ret2])


    elif data[userid]["status"] == "01":

        #首次填答問卷選擇【待改進】

        print('進入【首次填答待改進】')
        cat, Q = data[userid]["current"]
        ret = None
        last = len(get_category(cat, db))

        data[userid]["status"] = "00" #將值改回，避免下次跑進來
        data[userid]["Answered"][cat].append(Q)

        data[userid]["feedback"].append((cat, Q, text)) #紀錄(題號, 待改進內容)

        if Q == last:
            # ct_container = ct_push(data, userid, 1, 0) #~~~~~~~~~~~~~~~~~~~~~~~~

            output = data[userid]["feedback"]
            print('進入【(第一次)類別TEMPVIEW】──待改進的路')
            ret = cat_tempview_confirm(cat, output, db)#推第一次類別修改tempview confirm template
            # ct_container = ct_push(data, userid, 1, 0)

            # QC
            if cat == "Quick" and Q == last: #or ct_container == [Normal1, Indoors1, Corridor1, Outdoors1]:
                output = data[userid]["feedback"]
                ret = tempview_confirm(output, db)

        else:
            ret = [confirm(cat, Q, db)]

        line_bot_api.reply_message(
            event.reply_token, [TextSendMessage(text='『' + text + '』已收到回覆')] + ret)

    #類別/最終修改答案，告訴系統要改的題目(EG, C8)
    if data[userid]["status"] in ["10", "20"]:
        try:
            if revise_able(revise_extract(text)[0], revise_extract(text)[1]) is True:
                cat = revise_extract(text)[0]
                i   = revise_extract(text)[1]#相對題號

                # 禁止跨類別
                if cat == data[userid]["current"][0]:
                    data[userid]["current"] = (cat, i)

                    data[userid]['Answered'][cat].remove(i) #從已填答拿掉

                    newlist = []
                    for j in range(len(data[userid]["feedback"])):#從feedback拿掉要改的題的資料
                        if not(cat == data[userid]["feedback"][j][0] and i == data[userid]["feedback"][j][1]) :
                            newlist.append(data[userid]["feedback"][j])
                    data[userid]["feedback"] = newlist

                    #丟confirm
                    if data[userid]["status"] == "10":   #各類別要改答案
                        print('\n進入【類別修改答案】')
                        ret = [cat_revise_confirm(cat, i, db)]

                    elif data[userid]["status"] == "20":   # 最終要改答案
                        print('\n進入【最終修改答案】')
                        ret = [revise_confirm(cat, i, db)]

                    data[userid]["Answered"][cat].append(i)#加入已填答

                else:
                    ret = TextSendMessage(text="請修改當前類別：%s." % data[userid]["current"][0])

                line_bot_api.reply_message(event.reply_token, ret)

            else:
                ret = revise_idiot(text, revise_extract(text)[0], revise_extract(text)[1])
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text=ret))
        except:
            pass

    # 處理類別/最終改答案的時候，輸入的待改進的內容(EG, 哈囉MO)
    if data[userid]["status"] in ["11", "21"]:

        cat, Q = data[userid]["current"]
        data[userid]["feedback"].append((cat, Q, text)) # 紀錄(題號, 待改進內容)
        data[userid]["Answered"][cat].append(Q)
        output = data[userid]["feedback"]

        if data[userid]["status"] == "21": # 最終修改答案選待改進，revise_result會是false
            print('進入【最終修改待改進】')
            data[userid]["status"] = "20"

            ret = tempview_confirm(output, db)
            line_bot_api.reply_message(
                event.reply_token, [TextSendMessage(text='『' + text + '』已收到回覆')] + ret)

        elif data[userid]["status"] == "11": #類別修改答案選待改進，cat_revise_result會是false
            print('進入【類別修改待改進】')
            data[userid]["status"] = "10"

            ret = cat_tempview_confirm(cat, output, db)
            line_bot_api.reply_message(
                event.reply_token, [TextSendMessage(text='『' + text + '』已收到回覆')] + ret)


    if text == '我要設定帳號':
            ret = [
                TextSendMessage(text="此功能暫時關閉，若您有緊急事務，請洽詢水利署。"),
                StickerSendMessage(package_id=11537,sticker_id=52002770),
            ]

            line_bot_api.reply_message(event.reply_token, ret)
    #     if userid in get_userid_db(db): #已經填過了，問她要不要再改
    #         line_bot_api.reply_message(
    #             event.reply_token, account_confirm())
    #     elif userid not in get_userid_db(db): #第一次設
    #         account[userid] = {'userid':userid, 'name':0, 'county':0, 'school':0, 'phone':0}
    #         ret1 = TextSendMessage(text="【注意】：請一次設定完成")
    #         ret2 = TextSendMessage(text="請問您尊姓大名？")
    #         line_bot_api.reply_message(event.reply_token, [ret1] + [ret2])
    #         account_q = 1
    # elif account_q == 1:
    #     account[userid]['name'] = text
    #     ret = TextSendMessage(text="請問您的所在縣市？")
    #     line_bot_api.reply_message(event.reply_token, ret)
    #     account_q += 1
    # elif account_q == 2:
    #     text = '臺北市' if text == '台北市' else text
    #     account[userid]['county'] = text
    #     if text not in get_county_db(db):
    #         ret = TextSendMessage(text="不好意思，您所輸入的縣市不在我國疆域。提醒您中華民國採用繁體中文😁\n【請重新設定帳戶】")
    #         line_bot_api.reply_message(event.reply_token, ret)
    #         account.pop(userid)
    #         account_q = 0
    #     else:
    #         ret = TextSendMessage(text="請問您所在學校名稱為何？")
    #         line_bot_api.reply_message(event.reply_token, ret)
    #         account_q += 1
    # elif account_q == 3:
    #     account[userid]['school'] = text
    #     if text not in get_school_db(account[userid]['county'], db):
    #         ret = TextSendMessage(text="您的學校尚未與本平台合作，請聯絡我們")
    #         line_bot_api.reply_message(event.reply_token, ret)
    #         account.pop(userid)
    #         account_q = 0
    #     else:
    #         if text in no_repeat_school_db(account[userid]['county'], db):
    #             ret = TextSendMessage(text="您的學校已有負責人，請洽詢主管")
    #             line_bot_api.reply_message(event.reply_token, ret)
    #             account.pop(userid)
    #             account_q = 0
    #         else:
    #             account_q += 1
    #             ret = TextSendMessage(text="請問您的連絡電話？")
    #             line_bot_api.reply_message(event.reply_token, ret)
    # elif account_q == 4:
    #     account_q = 0
    #     account[userid]['phone'] = text
    #     ret = TextSendMessage(text="謝謝您的填答，您的身分已確認😁😁")
    #     line_bot_api.reply_message(event.reply_token, ret)
    #     get_account_db(account[userid], db)
    #     print(account[userid])

    ##################################
    ##########Postback Event#########
    ##################################

@handler.add(PostbackEvent)
def handle_postback(event):
    userid = event.source.user_id#取得Userid

    global account
    global account_q

    ##################################
    ########## 填問卷的過程 ###########
    ##################################

    #QC丟問題，相對題號
    if event.postback.data == 'Quick':
        line_bot_api.reply_message(
            event.reply_token, confirm_push(data, userid, event.postback.data, db))

    elif event.postback.data == 'Standard':
        ct_container = ct_push(data, userid, 1, 0, db)  #把4類別加進來
        carousel_template = CarouselTemplate(columns=ct_container)
        template_message = TemplateSendMessage(alt_text='詳細災情回覆問卷', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    #四類丟問題，相對題號
    elif event.postback.data in ['Normal', 'Indoors', 'Corridor', 'Outdoors']:
        line_bot_api.reply_message(
            event.reply_token, confirm_push(data, userid, event.postback.data, db))

    #戳題目的confirm template的時候
    try:
        parse = extract(event.postback.data) #[0]是類別；[1]是相對題號；[2]是沒問題/待改進
        cat, Q, ans = parse
        data[userid]["current"] = (cat, Q)
        ret = None
        last = len(get_category(cat, db))


        #處理carousel template
        #填完該類別最後一題且最後一題是沒問題
        if Q == last and ans == 'OK':
            data[userid]["status"] = "00"

            data[userid]["Answered"][cat].append(Q)
            output = data[userid]["feedback"]
            print('進入【(第一次)類別TEMPVIEW】')
            ret = cat_tempview_confirm(cat, output, db)#推第一次類別修改tempview confirm template
            ct_container = ct_push(data, userid, 1, 0, db)

            #QC填完
            if cat == "Quick" and Q == last:
                print('進入【(第一次)最終TEMPVIEW】──QC的路，不要怕上一句話，因為她是必經之路')
                output = data[userid]["feedback"]
                ret = tempview_confirm(output, db)#推第一次最終修改tempview confirm template


        #處理題目的confirm template
        #待改進的話，或是非該類別的最後一題
        else:
            ret, data[userid]["status"] = next(data, userid, parse, db)

        line_bot_api.reply_message(event.reply_token, ret)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('ERROR:', exc_type, exc_obj, fname, exc_tb.tb_lineno)
        print(event.postback.data)

        if event.postback.data == 'edit=NO':
            print('進入【最終修改答案不修改】，結束問卷')
            output = feedback.pop(userid) #填完了消滅它
            data.pop(userid)
            get_feedback(output, userid, db) #寫進資料庫

            ret = [
                TextSendMessage(text="已收到您的回覆～謝謝您的貢獻！"),
                StickerSendMessage(package_id=11537,sticker_id=52002739),
            ]

            line_bot_api.reply_message(event.reply_token, ret)

        if event.postback.data == 'edit=OK':
            print('進入【最終修改答案要修改】，要求輸入修改題號')
            data[userid]["status"] = "21" #表示【最終修改答案要修改】
            ret = [
                TextSendMessage(text="請問您要修改哪一題呢?"),
                TextSendMessage(text="【注意】：當您填寫快速檢核時，不能修改其他四類問題；反之亦然。"),
                TextSendMessage(text="請按照下列格式填寫：\n一般檢查(Normal)簡寫為N\n室內(Indoors)簡寫為I\n走廊(Corridor)簡寫為C\n室外(Outdoors)簡寫為O\n再加上題號，例如：\nN7(一般檢查的第七題)"),
            ]
            line_bot_api.reply_message(event.reply_token, ret)

        if event.postback.data == 'cat_edit=NO':
            print('進入【類別修改答案不修改】，丟出類別選單')
            ct_container = ct_push(data, userid, 1, 1, db)
            if ct_container == "All cats have already checked!": # 類別全部修改過後，進入最終環節
                print('進入【(第一次)最終TEMPVIEW】──標準填完了唷，不要怕上一句話，因為她是必經之路')
                output = data[userid]["feedback"]
                ret = tempview_confirm(output, db)
            else:
                carousel_template = CarouselTemplate(columns=ct_container)
                ret = TemplateSendMessage(alt_text='問卷選單', template=carousel_template)

            line_bot_api.reply_message(event.reply_token, ret)

        if 'cat_edit=OK' in event.postback.data:
            print('進入【類別修改答案要修改】，要求輸入修改題號')
            data[userid]["status"] = "10" #表示【類別修改答案要修改】

            ## 避免戳 Normal1, Indoors1, Corridor1, Outdoors1 的時候類別被鎖住
            cate = str(event.postback.data).split(';')[1] if ';' in event.postback.data else ''

            print('\n===<%s>===\n' % cate)
            relq = data[userid]["current"][1]
            data[userid]["current"] = (cate, relq) if cate != '' else data[userid]["current"]

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
        output = data[userid]["feedback"]
        ret = cat_tempview_confirm(data[userid]["current"][0], output, db)#把它目前的回答推個confirm template給他看看
        line_bot_api.reply_message(event.reply_token, ret)

    elif 'cat_revise=' in event.postback.data and 'NO' in event.postback.data:#待改進
        print('進入【類別修改答案待改進】，請簡述災情')
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="請簡述災情"))
        data[userid]["status"] = "11"

    ##################################
    ####### 最終修改答案的過程 #########
    ##################################

    if 'all_revise=' in event.postback.data and 'OK' in event.postback.data:#沒問題
        print('進入【最後修改答案沒問題】，丟出tempview')
        output = data[userid]["feedback"]
        ret = tempview_confirm(output, db)#把它目前的回答推個confirm template給他看看
        line_bot_api.reply_message(event.reply_token, ret)

    elif 'all_revise=' in event.postback.data and 'NO' in event.postback.data:#待改進
        print('進入【最後修改答案待改進】，請簡述災情')
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="請簡述災情"))
        data[userid]["status"] = "21"


    ##################################
    ########## 重設帳號或不設 #########
    ##################################

    if event.postback.data == 'account_reset':
        delete_userid_db(userid, db)
        account[userid] = {'userid':userid, 'name':0, 'county':0, 'school':0, 'phone':0}
        ret = TextSendMessage(text="請問您尊姓大名？")
        line_bot_api.reply_message(event.reply_token, ret)
        account_q = 1
    elif event.postback.data == 'account_remain':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="好的，謝謝😁"))
