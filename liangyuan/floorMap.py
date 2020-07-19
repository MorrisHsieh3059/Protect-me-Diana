from linebot import LineBotApi
from linebot.models import TextSendMessage, TemplateSendMessage, ConfirmTemplate, MessageTemplateAction, ButtonsTemplate, PostbackTemplateAction, URITemplateAction, CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn, ImageSendMessage, StickerSendMessage, LocationSendMessage, QuickReply, QuickReplyButton, MessageAction, FollowEvent, ImagemapSendMessage, BaseSize, MessageImagemapAction, URIImagemapAction, ImagemapArea, DatetimePickerTemplateAction

def sendE2Floor(event, line_bot_api):  # 圖片地圖
    try:
        message = [  # 串列
            TextSendMessage(  # 傳送文字
                text="請選擇檢查的樓層"
            ),
            ImagemapSendMessage(
                base_url='https://i.imgur.com/jYnxzhV.png',
                alt_text="This is the E2 floor's imagemap",
                base_size=BaseSize(height=1040, width=1040),
                actions=[
                    MessageImagemapAction(
                        text='E2-8F',
                        area=ImagemapArea(
                         x=0, y=90, width=1040, height=99
                        )
                    ),
                    MessageImagemapAction(
                        text='E2-7F',
                        area=ImagemapArea(
                            x=0, y=191, width=1040, height=79
                        )
                    ),
                    MessageImagemapAction(
                        text='E2-6F',
                        area=ImagemapArea(
                            x=0, y=273, width=1040, height=81
                        )
                    ),
                    MessageImagemapAction(
                        text='E2-5F',
                        area=ImagemapArea(
                            x=0, y=357, width=1040, height=77
                        )
                    ),
                    MessageImagemapAction(
                        text='E2-4F',
                        area=ImagemapArea(
                            x=0, y=437, width=1040, height=81
                        )
                    ),
                    MessageImagemapAction(
                        text='E2-3F',
                        area=ImagemapArea(
                            x=0, y=519, width=1040, height=83
                        )
                    ),
                    MessageImagemapAction(
                        text='E2-2F',
                        area=ImagemapArea(
                            x=0, y=604, width=1040, height=151
                        )
                    ),
                    MessageImagemapAction(
                        text='E2-1F',
                        area=ImagemapArea(
                            x=0, y=754, width=1040, height=206
                        )
                    ),
                    MessageImagemapAction(
                        text='E2-B1',
                        area=ImagemapArea(
                            x=0, y=963, width=1040, height=74
                        )
                    )
                ]
            )
        ]
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！sendFloorImgMap'))
