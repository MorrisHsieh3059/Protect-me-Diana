from linebot.models import (
    TemplateSendMessage, ConfirmTemplate, PostbackTemplateAction,
)

def confirm(cat, i, DB):
    questions = DB.get_category(cat)
    #這裡i 不用 -= 1 是因為data[userid][cat]是從 0開始計算
    return   TemplateSendMessage(
                alt_text='Confirm template',
                template=ConfirmTemplate(
                    text = str(questions[i][2]) + ' Q' + str(questions[i][3]) + ' : ' + questions[i][1],
                    actions=[
                        PostbackTemplateAction(
                            label='沒問題',
                            text=str(questions[i][2]) + ' 第' + str(questions[i][3]) + '題已回覆沒問題',  #給使用者看相對題號
                            data='cat=%s&no=%d&answer=OK' % (questions[i][2], questions[i][3]) #questions是整份問卷第幾題 絕對題號
                        ),
                        PostbackTemplateAction(
                            label='待改進',
                            text=str(questions[i][2]) + ' 第' + str(questions[i][3]) + '題已回覆待改進', #給使用者看相對題號
                            data='cat=%s&no=%d&answer=NO' % (questions[i][2], questions[i][3])
                        )
                    ]
                ))

    # 功能：從DB抓問題，編織成confirm tempate
    # 輸入：1.cat ： 類別
    #      2. i  ： 相對題號
    # 輸出：ConfirmTemplate with question
