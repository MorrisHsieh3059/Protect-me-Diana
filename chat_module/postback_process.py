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

def postback_process(userid, data, DB, event):
    """
        input:
            1. userid
            2. data
            3. DB
            4. event
        return:
            1. [message]
    """
    ret = "NA"
    user_data = data.get_user(userid)

    # 填問卷的過程
    # QC丟問題，相對題號
    if event.postback.data == 'Quick':
        ret = [confirm_push(data.get_all_users(), userid, event.postback.data, DB)]

    elif event.postback.data == 'Standard':
        ct_container = ct_push(data.get_all_users(), userid, 1, 0, DB)  #把4類別加進來
        carousel_template = CarouselTemplate(columns=ct_container)
        ret = [TemplateSendMessage(alt_text='詳細災情回覆問卷', template=carousel_template)]

    # 四類丟問題，相對題號
    elif event.postback.data in ['Normal', 'Indoors', 'Corridor', 'Outdoors']:
        ret = [confirm_push(data.get_all_users(), userid, event.postback.data, DB)]

    # 戳題目的confirm template的時候
    try:
        parse = extract(event.postback.data) # [0]是類別；[1]是相對題號；[2]是沒問題/待改進
        cat, Q, ans = parse
        data.set_user_current(userid, (cat, Q))
        last = len(DB.get_category(cat))

        # 處理carousel template
        # 填完該類別最後一題且最後一題是沒問題
        if Q == last and ans == 'OK':
            data.set_user_status(userid, "00")
            data.add_user_answered(userid, cat, Q)
            output = data.get_user_feedback(userid)

            print('進入【(第一次)類別TEMPVIEW】')
            print(f"\n\n====\ncat: |{cat}\nOutput: |{output}\n")
            ret = cat_tempview_confirm(cat, output, DB) # 推第一次類別修改tempview confirm template
            # ct_container = ct_push(data.get_all_users(), userid, 1, 0, DB)

            # QC填完
            if cat == "Quick" and Q == last:
                print('進入【最終TEMPVIEW】──QC的路，不要怕上一句話，因為她是必經之路')
                output = data.get_user_feedback(userid)
                ret = tempview_confirm(output, DB) # 推第一次最終修改tempview confirm template

        # 處理題目的confirm template
        # 待改進的話，或是非該類別的最後一題
        else:
            ret = [next(data.get_all_users(), userid, parse, DB)[0]]
            status = next(data.get_all_users(), userid, parse, DB)[1]
            data.set_user_status(userid, status)

    except Exception as e:
        # exc_type, exc_obj, exc_tb = sys.exc_info()
        # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # print('ERROR:', exc_type, exc_obj, fname, exc_tb.tb_lineno)
        # print(event.postback.data)

        if event.postback.data == 'edit=NO':
            data.set_user_status(userid, "00")
            output = data.get_user_feedback(userid)
            print(f"\n\n\nAARRR!!!{output}\n\n\n")
            build, room = data.get_user_building(userid)
            print(f"\n\n\nBBRRR!!!{(build, room)}\n\n\n")
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

            data.remove_user(userid)

        if event.postback.data == 'edit=OK':
            print('進入【最終修改答案要修改】，要求輸入修改題號')
            data.set_user_status(userid, "20")
            ret = [
                TextSendMessage(text="請問您要修改哪一題呢?"),
                TextSendMessage(text="【注意】：當您填寫快速檢核時，不能修改其他四類問題；反之亦然。"),
                TextSendMessage(text="請按照下列格式填寫：\n一般檢查(Normal)簡寫為N\n室內(Indoors)簡寫為I\n走廊(Corridor)簡寫為C\n室外(Outdoors)簡寫為O\n再加上題號，例如：\nN7(一般檢查的第七題)"),
            ]

        if event.postback.data == 'cat_edit=NO':
            print('進入【類別修改答案不修改】，丟出類別選單')
            ct_container = ct_push(data.get_all_users(), userid, 1, 1, DB)
            if ct_container == "All cats have already checked!": # 類別全部修改過後，進入最終環節
                print('進入【最終TEMPVIEW】──標準填完了唷，不要怕上一句話，因為她是必經之路')
                output = data.get_user_feedback(userid)
                ret = tempview_confirm(output, DB)
            else:
                carousel_template = CarouselTemplate(columns=ct_container)
                ret = [TemplateSendMessage(alt_text='問卷選單', template=carousel_template)]

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

    # 類別修改答案的過程
    if 'cat_revise=' in event.postback.data and 'OK' in event.postback.data: # 沒問題
        print('進入【類別修改答案沒問題】，丟出cat_tempview')
        output = data.get_user_feedback(userid)
        ret = cat_tempview_confirm(user_data["current"][0], output, DB) # 把它目前的回答推個confirm template給他看看

    elif 'cat_revise=' in event.postback.data and 'NO' in event.postback.data: # 待改進
        print('進入【類別修改答案待改進】，請簡述災情')
        ret = [TextSendMessage(text="請簡述災情")]
        data.set_user_status(userid, "11")

    # 最終修改答案的過程
    if 'all_revise=' in event.postback.data and 'OK' in event.postback.data: # 沒問題
        print('進入【最後修改答案沒問題】，丟出tempview')
        output = data.get_user_feedback(userid)
        ret = tempview_confirm(output, DB) # 把它目前的回答推個confirm template給他看看

    elif 'all_revise=' in event.postback.data and 'NO' in event.postback.data: # 待改進
        print('進入【最後修改答案待改進】，請簡述災情')
        ret = [TextSendMessage(text="請簡述災情")]
        data.set_user_status(userid, "21")

    # 重設帳號或不設
    if event.postback.data == 'account_reset':
        delete_userid_db(userid, DB)
        account[userid] = {'userid':userid, 'name':0, 'county':0, 'school':0, 'phone':0}
        ret = [TextSendMessage(text="請問您尊姓大名？")]
        account_q = 1

    elif event.postback.data == 'account_remain':
        ret = [TextSendMessage(text="好的，謝謝😁")]

    return ret
