from linebot import LineBotApi
from linebot.models import TextSendMessage, TemplateSendMessage, ConfirmTemplate, MessageTemplateAction, ButtonsTemplate, PostbackTemplateAction, URITemplateAction, CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn, ImageSendMessage, StickerSendMessage, LocationSendMessage, QuickReply, QuickReplyButton, MessageAction, FollowEvent, ImagemapSendMessage, BaseSize, MessageImagemapAction, URIImagemapAction, ImagemapArea, DatetimePickerTemplateAction

def send_E2_4F_classroom(event, line_bot_api):  # 確認按鈕模板
    try:
        print(event)
        Confirm_template = TemplateSendMessage(
            alt_text="This is E2 4F classroom confirm template",
            template=ConfirmTemplate(
                title='This is a ConfirmTemplate',
                text='請問要檢查E2工程二館\n4F哪一側？',  # 要問的問題，或是文字敘述
                # action 最多只能兩個喔！
                actions=[
                    MessageAction(
                      label='西側',  # 顯示名稱
                      text='西側'  # 點擊後，回傳的文字
                    ),
                    MessageAction(
                        label='東側',  # 顯示名稱
                        text='東側'  # 點擊後，回傳的文字
                    )
                ]
            )
        )
        print("1235952")
        line_bot_api.reply_message(event.reply_token, Confirm_template)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            text='發生錯誤！send_E2_4F_classroom'))

def send_E2_4F_East_classroom(event, line_bot_api):  # 圖片地圖
    try:
        imagemap_message = ImagemapSendMessage(
            base_url='https://i.imgur.com/AUIICvS.png',
            alt_text="This is the E2 4F East classroom's imagemap",
            base_size=BaseSize(height=1040, width=1040),
            actions=[
                MessageImagemapAction(
                    text='E2-412教學電腦室',
                    area=ImagemapArea(
                        x=78, y=798, width=377, height=207
                    )
                ),
                MessageImagemapAction(
                    text='E2-413研究室',
                    area=ImagemapArea(
                        x=78, y=714, width=377, height=78
                    )
                ),
                MessageImagemapAction(
                    text='E2-414研究室',
                    area=ImagemapArea(
                        x=78, y=630, width=377, height=77
                    )
                ),
                MessageImagemapAction(
                    text='E2-415研究室',
                    area=ImagemapArea(
                        x=78, y=543, width=377, height=78
                    )
                ),
                MessageImagemapAction(
                    text='E2-416研究室',
                    area=ImagemapArea(
                        x=78, y=455, width=377, height=83
                    )
                ),
                MessageImagemapAction(
                    text='E2-417研究室',
                    area=ImagemapArea(
                        x=78, y=373, width=377, height=77
                    )
                ),
                MessageImagemapAction(
                    text='E2-418研究室',
                    area=ImagemapArea(
                        x=78, y=288, width=377, height=77
                    )
                ),
                MessageImagemapAction(
                    text='E2-419研究室',
                    area=ImagemapArea(
                        x=78, y=201, width=377, height=79
                    )
                ),
                MessageImagemapAction(
                    text='E2-420儲藏室',
                    area=ImagemapArea(
                        x=316, y=30, width=137, height=165
                    )
                ),
                MessageImagemapAction(
                    text='女廁',
                    area=ImagemapArea(
                        x=186, y=32, width=119, height=163
                    )
                ),
                MessageImagemapAction(
                    text='男廁',
                    area=ImagemapArea(
                        x=78, y=32, width=98, height=164
                    )
                ),
                MessageImagemapAction(
                    text='E2-406網路控制室',
                    area=ImagemapArea(
                        x=705, y=201, width=215, height=251
                    )
                ),
                MessageImagemapAction(
                    text='E2-407教授研究室',
                    area=ImagemapArea(
                        x=705, y=457, width=215, height=79
                    )
                ),
                MessageImagemapAction(
                    text='E2-408教授研究室',
                    area=ImagemapArea(
                        x=705, y=543, width=215, height=79
                    )
                ),
                MessageImagemapAction(
                    text='E2-409教授研究室',
                    area=ImagemapArea(
                        x=705, y=630, width=215, height=78
                    )
                ),
                MessageImagemapAction(
                    text='E2-410教授研究室',
                    area=ImagemapArea(
                        x=705, y=714, width=215, height=78
                    )
                ),
                MessageImagemapAction(
                    text='E2-411教授研究室',
                    area=ImagemapArea(
                        x=705, y=799, width=215, height=78
                    )
                ),
                MessageImagemapAction(
                    text='E2-4F東側樓梯間',
                    area=ImagemapArea(
                        x=705, y=884, width=213, height=121
                    )
                )
            ]
        )
        line_bot_api.reply_message(event.reply_token, imagemap_message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            text='發生錯誤！send_E2_4F_East_classroom'))

def send_E2_4F_West_classroom(event, line_bot_api):  # 圖片地圖
    try:
        imagemap_message = ImagemapSendMessage(
            base_url='https://i.imgur.com/AUIICvS.png',
            alt_text="This is the E2 4F West classroom's imagemap",
            base_size=BaseSize(height=1040, width=1040),
            actions=[
                MessageImagemapAction(
                    text='E2-412教學電腦室',
                    area=ImagemapArea(
                        x=78, y=798, width=377, height=207
                    )
                ),
                MessageImagemapAction(
                    text='E2-413研究室',
                    area=ImagemapArea(
                        x=78, y=714, width=377, height=78
                    )
                ),
                MessageImagemapAction(
                    text='E2-414研究室',
                    area=ImagemapArea(
                        x=78, y=630, width=377, height=77
                    )
                ),
                MessageImagemapAction(
                    text='E2-415研究室',
                    area=ImagemapArea(
                        x=78, y=543, width=377, height=78
                    )
                ),
                MessageImagemapAction(
                    text='E2-416研究室',
                    area=ImagemapArea(
                        x=78, y=455, width=377, height=83
                    )
                ),
                MessageImagemapAction(
                    text='E2-417研究室',
                    area=ImagemapArea(
                        x=78, y=373, width=377, height=77
                    )
                ),
                MessageImagemapAction(
                    text='E2-418研究室',
                    area=ImagemapArea(
                        x=78, y=288, width=377, height=77
                    )
                ),
                MessageImagemapAction(
                    text='E2-419研究室',
                    area=ImagemapArea(
                        x=78, y=201, width=377, height=79
                    )
                ),
                MessageImagemapAction(
                    text='E2-420儲藏室',
                    area=ImagemapArea(
                        x=316, y=30, width=137, height=165
                    )
                ),
                MessageImagemapAction(
                    text='女廁',
                    area=ImagemapArea(
                        x=186, y=32, width=119, height=163
                    )
                ),
                MessageImagemapAction(
                    text='男廁',
                    area=ImagemapArea(
                        x=78, y=32, width=98, height=164
                    )
                ),
                MessageImagemapAction(
                    text='E2-406網路控制室',
                    area=ImagemapArea(
                        x=705, y=201, width=215, height=251
                    )
                ),
                MessageImagemapAction(
                    text='E2-407教授研究室',
                    area=ImagemapArea(
                        x=705, y=457, width=215, height=79
                    )
                ),
                MessageImagemapAction(
                    text='E2-408教授研究室',
                    area=ImagemapArea(
                        x=705, y=543, width=215, height=79
                    )
                ),
                MessageImagemapAction(
                    text='E2-409教授研究室',
                    area=ImagemapArea(
                        x=705, y=630, width=215, height=78
                    )
                ),
                MessageImagemapAction(
                    text='E2-410教授研究室',
                    area=ImagemapArea(
                        x=705, y=714, width=215, height=78
                    )
                ),
                MessageImagemapAction(
                    text='E2-411教授研究室',
                    area=ImagemapArea(
                        x=705, y=799, width=215, height=78
                    )
                ),
                MessageImagemapAction(
                    text='E2-4F東側樓梯間',
                    area=ImagemapArea(
                        x=705, y=884, width=213, height=121
                    )
                )
            ]
        )
        line_bot_api.reply_message(event.reply_token, imagemap_message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            text='發生錯誤！send_E2_4F_West_classroom'))
