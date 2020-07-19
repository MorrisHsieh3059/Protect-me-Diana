from linebot.models import (
TextSendMessage, TemplateSendMessage, CarouselTemplate, StickerSendMessage,
)

from questionnaire.extract_function import extract, revise_extract       #RE抓數字
from questionnaire.ct_push import ct_push               #抓推播新的carousel template
from questionnaire.confirm import confirm          #抓confirm template 進來
from questionnaire.carousel import *               #抓caousel columns
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

from liangyuan.func import *
from chat_module.ner.demo import ner_sent, ques_and_ans

def text_process(text, userid, data, DB, event):
    """
        input:
            1. text: request
            2. userid
            3. data: user's status
            4. DB: database
            5. event: just for liangyuan
        return:
            1. [message]
    """
    user_data = data.get_user(userid)
    ret = "NA"

    if text == '我要設定帳號':
        ret = [
            TextSendMessage(text="此功能暫時關閉。"),
            StickerSendMessage(package_id=11537,sticker_id=52002770),
        ]

    elif text == '請給我使用須知':
        ret1 = TextSendMessage(text="歡迎使用本平台😁\n本平台是作為學校校安機關的安全檢核系統\n目前功能僅有表單檢核功能")
        ret2 = TextSendMessage(text="【填寫表單須知】：\n您可以透過點選選單中的問卷按鈕，或是輸入「問卷」來呼叫問卷。\n本問卷提供兩種填答方式：\n\n1.快速檢核：若情況緊急，請使用此捷徑\n2.常規問卷：共分成四類選單，可交叉填答\n【注意】：兩種填寫方式不可交叉填寫")
        ret3 = TextSendMessage(text="本次填寫的事件為：" + str(DB.get_latest_assessment_id_db()[1]))
        ret = ([ret1] + [ret2] + [ret3])

    elif text == '我要統計資料' or text == 'I need the summary of inspection results.':
        ret = [TextSendMessage(text="https://pmdiana.hcilab.katrina.tw/report/index.html")]

    # Questionnaire Process
    if userid not in data.get_all_users() and userid not in DB.get_yitianda_db():
        data.add_user(userid)
        # print("新用戶!")

    if userid in DB.get_yitianda_db():
        ret1 = TextSendMessage(text="您已為本次事件提供災情回覆咯~")
        ret2 = TextSendMessage(text="本次填寫的事件為：" + str(DB.get_latest_assessment_id_db()[1]))
        ret = [ret1] + [ret2]

    else:
        ### Module 1: liangyuan ###
        if data.get_user_status(userid) == "pre":
            print("第一模組")
            signal = toCheck(event, line_bot_api)
            data.set_user_status(userid, signal[0])
            if signal[1] != "": # Record building name
                # building_id = DB.get_building_id(signal[1])
                # print(building_id)
                data.set_user_building(userid, signal[1]) # 紀錄建築名字
            ret = "NOREPLY"

        ### Module 2 ###
        elif data.get_user_status(userid) == "pre-class": # module 1 跟 2 的街口
            if data.get_user_current(userid) == (): # 第一次填寫的時候
                line_bot_api.unlink_rich_menu_from_user(userid)
                ct_container = ct_push(data.get_all_users(), userid, 0, 0, DB) # 前面ㄉ0代表推出【快速/標準carousel】
                                                               # 後面ㄉ0代表非(類別不修改)
                data.set_user_status(userid, "00")
                data.set_user_building(userid, text) # 紀錄教室名字

                carousel_template = CarouselTemplate(columns=ct_container)
                ret = [TemplateSendMessage(alt_text='災情回覆問卷', template=carousel_template)]

            elif user_data['Answered']['Quick'] != []: #選擇快速檢核後，阻止其跳回標準檢核
                ret = [TextSendMessage(text="您已選擇快速檢核！請填頁面上的最後一題")]

            else:
                ct_container = ct_push(data.get_all_users(), userid, 1, 0, DB) #1代表推出【四大題組carousel】
                carousel_template = CarouselTemplate(columns=ct_container)
                ret = [TemplateSendMessage(alt_text='問卷選單', template=carousel_template)]

        elif user_data["status"] == "01" and "題已回覆" not in text:
            #首次填答問卷選擇【待改進】
            print('進入【首次填答待改進】')
            cat = user_data["current"][0]
            Q = user_data["current"][1]
            ret = None

            data.add_user_answered(userid, cat, Q)
            _ = data.get_user_current(userid)
            if len(_) == 2:
                _ += (text,)
            else:
                _ = (_[0], _[1], text,)
            data.set_user_current(userid, _)
            data.add_user_feedback(userid, (cat, Q, text))

            # ner check --------------------------------------------------------
            # ent_q = questions_ent[cat][Q] # raw_text = DB.get_category(cat)[Q][1]
            # ent_a = ner_sent(text)
            # ent = ques_and_ans(ent_q, ent_a)
            ent = ner_sent(text)
            if not (len(ent["event"]) > 0 and len(ent["location"]) > 0 and len(ent["product_name"]) > 0):
                complement = []
                if len(ent["event"]) == 0:
                    complement.append("事件")
                if len(ent["location"]) == 0:
                    complement.append("地點")
                if len(ent["product_name"]) == 0:
                    complement.append("物品名稱")
                ret = ([TextSendMessage(text=f"請提供{complement}！")])
            else:
                # --------------------------------------------------------------
                # 請使用者點選問題所在位置
                floor = floor_plan()
                ret = ([TextSendMessage(text='『' + text + '』已收到回覆')] + [TextSendMessage(text="請點選問題所在位置(九宮格)")] + [floor])
                data.set_user_status(userid, "02") # 等待使用者戳點

        # 使用者要戳 平面圖
        elif user_data["status"] == "02":
            if text in ['上左', '上中', '上右', '中左', '中中', '中右', '下左', '下中', '下右']:
                data.set_user_spec_feedback_pos(userid, text)
                _ = data.get_user_current(userid) + (text,)
                data.set_user_current(userid, _)

                data.set_user_status(userid, "03") # 等他傳照片
                ret = [TextSendMessage(text="請傳照片，並稍後照片上傳時間(約數秒)🙏")]
            else:
                ret = [TextSendMessage(text="請點選上方平面圖！")]

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

                        else:
                            print(f"\n\n\n\n\nAARRRRRRRRRRRRRRRRRRR\n待改進不是類別也不是最終\n\n\n\n")
                        data.add_user_answered(userid, cat, i)

                    else:
                        ret = [TextSendMessage(text="請修改當前類別：%s." % user_data["current"][0])]

                else:
                    ret = [TextSendMessage(text=revise_idiot(text, revise_extract(text)[0], revise_extract(text)[1]))]
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

    return ret
