from linebot.models import (
    TextSendMessage, StickerSendMessage,
    TemplateSendMessage, ConfirmTemplate, PostbackTemplateAction,
)
from .get_question_db import get_all            #DB抓問題

def takeFirst(elem):
    return elem[0]

def tempview(output, db):
    questions = get_all(db)
    render = []

    output.sort(key=takeFirst)

    for i, value in output:
        i -= 1 #題號校正
        display = """題目：{} Q{}({})
回覆：{}""".format(questions[i][2], str(questions[i][3]), questions[i][1], value)
        render.append(display)

    return """您好，您的回覆如下：

{}

未顯示之題目為『沒問題』

【注意】：當您填寫快速檢核時，不能修改其他四類問題；反之亦然。""".format('\n\n'.join(render))

    # 功能：給他暫時看看他剛剛到底說了什麼要待改進的東西
    # 輸入：output = feedback[userid]
    # 輸出：str (他所回覆要待改進的內容)

def tempview_confirm(output, db):
    ret = [
        StickerSendMessage(package_id=2,sticker_id=150),
        TextSendMessage(text=tempview(output, db)),
        TemplateSendMessage(
                    alt_text='Confirm template',
                    template=ConfirmTemplate(
                        text = '請問您要修改您的回答嗎？',
                        actions=[
                            PostbackTemplateAction(
                                label='要',
                                text='我要修改我的答案',  #給使用者看相對題號
                                data='edit=OK' #questions是整份問卷第幾題 絕對題號
                            ),
                            PostbackTemplateAction(
                                label='不要',
                                text='我已確認沒問題', #給使用者看相對題號
                                data='edit=NO'
                            )
                        ]
                    ))
    ]
    return ret

def cat_tempview(cat, output, db):

    num = []
    num = list(range(1,13)) if cat == 'Normal' else num
    num = list(range(13,33)) if cat == 'Indoors' else num
    num = list(range(33,46)) if cat == 'Corridor' else num
    num = list(range(46,65)) if cat == 'Outdoors' else num

    newoutput = []
    for i in output:
        if i[0] in num:
            newoutput.append(i)
    output = newoutput

    questions = get_all(db)
    render = []

    output.sort(key=takeFirst)

    for i, value in output:
        i -= 1 #題號校正
        display = """題目：{} Q{}({})
回覆：{}""".format(questions[i][2], str(questions[i][3]), questions[i][1], value)
        render.append(display)

    return """您好，您的回覆如下：

{}

未顯示之題目為『沒問題』""".format('\n\n'.join(render))

def cat_tempview_confirm(cat, output, db):
    ret = [
        TextSendMessage(text=cat_tempview(cat, output, db)),
        TemplateSendMessage(
                    alt_text='Confirm template',
                    template=ConfirmTemplate(
                        text = '請問您要修改這個類別的答案嗎？',
                        actions=[
                            PostbackTemplateAction(
                                label='要',
                                text='我要修改我的答案',  #給使用者看相對題號
                                data='cat_edit=OK' #questions是整份問卷第幾題 絕對題號
                            ),
                            PostbackTemplateAction(
                                label='不要',
                                text='我已確認沒問題', #給使用者看相對題號
                                data='cat_edit=NO'
                            )
                        ]
                    ))
    ]
    return ret
