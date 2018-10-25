from __future__ import unicode_literals
import errno
import os
import sys
import tempfile
from argparse import ArgumentParser
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction, PostbackTemplateAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton
)

app = Flask(__name__)
##################################

line_bot_api = LineBotApi("apQkyD5cnxa8kanS8yfnr+ExfDR/yUoKmLXVu7epNzWsXqIoD1twn/YCGRnhIZLv4r36JYsjzVlpfWMHHaoTs9V4d/somxpkAI0ZNpiG8axYMp+xMbVvcC5vwyKEGizJWZ4CK1KX5DFqVxe5mb5lPgdB04t89/1O/w1cDnyilFU=", "http://localhost:8080")
handler = WebhookHandler("e1af475f2498d7d75ecceca445f69bf7")

toM = "Uf06239f6f01f24d5664045d8333ab49d"

image_url_1 = "https://sdl-stickershop.line.naver.jp/stickershop/v1/sticker/60932570/android/sticker.png"
image_url_2 = "https://stickershop.line-scdn.net/stickershop/v1/sticker/11482775/ANDROID/sticker.png"
image_url_3 = "https://stickershop.line-scdn.net/stickershop/v1/product/9601/LINEStorePC/main@2x.png;compress=true"
image_url_4 = "https://sdl-stickershop.line.naver.jp/stickershop/v1/sticker/11482762/android/sticker.png"
image_url_5 = "https://stickershop.line-scdn.net/stickershop/v1/product/1040299/LINEStorePC/main@2x.png;compress=true"


Normal1 = CarouselColumn(
                    thumbnail_image_url=image_url_2,
                    title='Normal',
                    text='這是一般性檢查',
                    actions=[
                        PostbackTemplateAction(
                            label='開始填寫',
                            #text='postback text1',
                            data='Normal'
                        )
                    ]
                )
Normal2 = CarouselColumn(
                    thumbnail_image_url=image_url_2,
                    title='Normal',
                    text='這是一般性檢查',
                    actions=[
                        PostbackTemplateAction(
                            label='已經填寫了~',
                            #text='postback text1',
                            data=''
                        )
                    ]
                )
Indoors1 = CarouselColumn(
                    thumbnail_image_url=image_url_2,
                    title='Indoors',
                    text='這是門/窗/牆/天花板/柱/地板',
                    actions=[
                        PostbackTemplateAction(
                            label='開始填寫',
                            #text='postback text1',
                            data='Indoors'
                        )
                    ]
                )
Indoors2 = CarouselColumn(
                    thumbnail_image_url=image_url_2,
                    title='Indoors',
                    text='這是門/窗/牆/天花板/柱/地板',
                    actions=[
                        PostbackTemplateAction(
                            label='已經填寫了~',
                            #text='postback text1',
                            data=''
                        )
                    ]
                )
Corridor1 = CarouselColumn(
                    thumbnail_image_url=image_url_2,
                    title='Corridor',
                    text='這是欄杆/樓梯/走廊',
                    actions=[
                        PostbackTemplateAction(
                            label='開始填寫',
                            #text='postback text1',
                            data='Corridor'
                        )
                    ]
                )
Corridor2 = CarouselColumn(
                    thumbnail_image_url=image_url_2,
                    title='Corridor',
                    text='這是欄杆/樓梯/走廊',
                    actions=[
                        PostbackTemplateAction(
                            label='已經填寫了~',
                            #text='postback text1',
                            data=''
                        )
                    ]
                )
Outdoors1 = CarouselColumn(
                    thumbnail_image_url=image_url_2,
                    title='Outdoors',
                    text='這是地基/屋頂/管線/消防',
                    actions=[
                        PostbackTemplateAction(
                            label='開始填寫',
                            #text='postback text1',
                            data='Outdoors'
                        )
                    ]
                )
Outdoors2 = CarouselColumn(
                    thumbnail_image_url=image_url_2,
                    title='Outdoors',
                    text='這是地基/屋頂/管線/消防',
                    actions=[
                        PostbackTemplateAction(
                            label='已經填寫了~',
                            #text='postback text1',
                            data=''
                        )
                    ]
                )


#####################

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

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


    if text == 'carousel':
        carousel_template = CarouselTemplate(columns=[Normal1, Normal2, Indoors1, Indoors2, Corridor1, Corridor2, Outdoors1, Outdoors2])
        template_message = TemplateSendMessage(alt_text='MoMo', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    else:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text))
