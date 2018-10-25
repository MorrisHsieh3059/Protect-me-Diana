##################################
#########   Just Import  #########
##################################


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

from class_DB import DB
from extract_function import *

app = Flask(__name__)

##################################
##########  Good Simu   ##########
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
                            text='Normal',
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
                            data='已經填寫了~'
                        )
                    ]
                )
Indoors1 = CarouselColumn(
                    thumbnail_image_url=image_url_3,
                    title='Indoors',
                    text='這是門/窗/牆/天花板/柱/地板',
                    actions=[
                        PostbackTemplateAction(
                            label='開始填寫',
                            text='Indoors',
                            data='Indoors'
                        )
                    ]
                )
Indoors2 = CarouselColumn(
                    thumbnail_image_url=image_url_3,
                    title='Indoors',
                    text='這是門/窗/牆/天花板/柱/地板',
                    actions=[
                        PostbackTemplateAction(
                            label='已經填寫了~',
                            #text='postback text1',
                            data='已經填寫了~'
                        )
                    ]
                )
Corridor1 = CarouselColumn(
                    thumbnail_image_url=image_url_4,
                    title='Corridor',
                    text='這是欄杆/樓梯/走廊',
                    actions=[
                        PostbackTemplateAction(
                            label='開始填寫',
                            text='Corridor',
                            data='Corridor'
                        )
                    ]
                )
Corridor2 = CarouselColumn(
                    thumbnail_image_url=image_url_4,
                    title='Corridor',
                    text='這是欄杆/樓梯/走廊',
                    actions=[
                        PostbackTemplateAction(
                            label='已經填寫了~',
                            #text='postback text1',
                            data='已經填寫了~'
                        )
                    ]
                )
Outdoors1 = CarouselColumn(
                    thumbnail_image_url=image_url_5,
                    title='Outdoors',
                    text='這是地基/屋頂/管線/消防',
                    actions=[
                        PostbackTemplateAction(
                            label='開始填寫',
                            text='Outdoors',
                            data='Outdoors'
                        )
                    ]
                )
Outdoors2 = CarouselColumn(
                    thumbnail_image_url=image_url_5,
                    title='Outdoors',
                    text='這是地基/屋頂/管線/消防',
                    actions=[
                        PostbackTemplateAction(
                            label='已經填寫了~',
                            #text='postback text1',
                            data='已經填寫了~'
                        )
                    ]
                )




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
        carousel_template = CarouselTemplate(columns=[Normal1, Indoors1, Corridor1, Outdoors1])
        template_message = TemplateSendMessage(alt_text='問卷選單', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    else:
        pass


##################################
#########Confirm Template#########
##################################
data = {}


def confirm(cat, i):
    db = DB()
    questions = db.get_category(cat)
    return   TemplateSendMessage(
                alt_text='Confirm template',
                template=ConfirmTemplate(
                    text = questions[i][1],
                    actions=[
                        PostbackTemplateAction(
                            label='沒問題',
                            text='沒問題',
                            data='no=' + str(questions[i][0]) + '&answer=OK' #questions是整份問卷第幾題 相對題號
                        ),
                        PostbackTemplateAction(
                            label='待改進',
                            text='待改進',
                            data='no=' + str(questions[i][0]) + '&answer=NO'
                        )
                    ]
                ))

##################################
##########Postback Event##########
##################################

@handler.add(PostbackEvent)

def handle_postback(event):
    userid = event.source.user_id#取得Userid


    #Normal丟問題，相對題號
    if event.postback.data == 'Normal':
        if userid in data and data[userid]['Normal'] != 0:#在裡面的話+1
            data[userid]['Normal'] += 1
        else:
            data[userid] = {"Normal":0, "Indoors":0, "Corridor":0, "Outdoors":0}#不在裡面的話add key
        line_bot_api.reply_message(
            event.reply_token, confirm("Normal",data[userid]['Normal']))

    #Indoors丟問題，相對題號
    elif event.postback.data == 'Indoors':
        if userid in data and data[userid]['Indoors'] != 0:#在裡面的話+1
            data[userid]['Indoors'] += 1
        else:
            data[userid] = {"Normal":0, "Indoors":0, "Corridor":0, "Outdoors":0}#不在裡面的話add key
        line_bot_api.reply_message(
            event.reply_token, confirm("Indoors",data[userid]['Indoors']))

    #Corridor丟問題，相對題號
    elif event.postback.data == 'Corridor':
        if userid in data and data[userid]['Corridor'] != 0:#在裡面的話+1
            data[userid]['Corridor'] += 1
        else:
            data[userid] = {"Normal":0, "Indoors":0, "Corridor":0, "Outdoors":0}#不在裡面的話add key
        line_bot_api.reply_message(
            event.reply_token, confirm("Corridor",data[userid]['Corridor']))

    #Outdoors丟問題，相對題號
    elif event.postback.data == 'Outdoors':
        if userid in data and data[userid]['Outdoors'] != 0:#在裡面的話+1
            data[userid]['Outdoors'] += 1
        else:
            data[userid] = {"Normal":0, "Indoors":0, "Corridor":0, "Outdoors":0}#不在裡面的話add key
        line_bot_api.reply_message(
            event.reply_token, confirm("Outdoors",data[userid]['Outdoors']))


    #從 Confirm 收到Normal 1-11題，自訂函數 extract
    elif extract(event.postback.data) in list(range(1,12)):
        data[userid]['Normal'] += 1
        line_bot_api.reply_message(
            event.reply_token, confirm("Normal",data[userid]['Normal']))

    #從 Confirm 收到Indoors 13-32題，自訂函數 extract
    elif extract(event.postback.data) in list(range(13,32)):
        data[userid]['Indoors'] += 1
        line_bot_api.reply_message(
            event.reply_token, confirm("Indoors",data[userid]['Indoors']))

    #從 Confirm 收到Corridor 33-45題，自訂函數 extract
    elif extract(event.postback.data) in list(range(33,45)):
        data[userid]['Corridor'] += 1
        line_bot_api.reply_message(
            event.reply_token, confirm("Corridor",data[userid]['Corridor']))

    #從 Confirm 收到Outdoors 46-64題，自訂函數 extract
    elif extract(event.postback.data) in list(range(46,64)):
        data[userid]['Outdoors'] += 1
        line_bot_api.reply_message(
            event.reply_token, confirm("Outdoors",data[userid]['Outdoors']))



    #如果Confirm收到12(Normal的最後一題)的話要跳回去Ct
    elif extract(event.postback.data) == 12:#絕對題數
        ct_container = []
        ct_container.append(Normal2)

        if data[userid]['Indoors'] == 20:#該類題數
            ct_container.append(Indoors2)
        else:
            ct_container.append(Indoors1)

        if data[userid]['Corridor'] == 13:#該類題數
            ct_container.append(Corridor2)
        else:
            ct_container.append(Corridor1)

        if data[userid]['Outdoors'] == 19:#該類題數
            ct_container.append(Outdoors2)
        else:
            ct_container.append(Outdoors1)

        carousel_template = CarouselTemplate(columns=ct_container)
        template_message = TemplateSendMessage(alt_text='問卷選單', template=carousel_template)
        #把CT推出去
        line_bot_api.reply_message(
            event.reply_token, template_message)


    #如果Confirm收到32(Indoors的最後一題)的話要跳回去Ct
    elif extract(event.postback.data) == 32:#絕對題數
        ct_container = []
        ct_container.append(Indoors2)

        if data[userid]['Normal'] == 12:#該類題數
            ct_container.append(Normal2)
        else:
            ct_container.append(Normal1)

        if data[userid]['Corridor'] == 13:#該類題數
            ct_container.append(Corridor2)
        else:
            ct_container.append(Corridor1)

        if data[userid]['Outdoors'] == 19:#該類題數
            ct_container.append(Outdoors2)
        else:
            ct_container.append(Outdoors1)

        carousel_template = CarouselTemplate(columns=ct_container)
        template_message = TemplateSendMessage(alt_text='問卷選單', template=carousel_template)
        #把CT推出去
        line_bot_api.reply_message(
            event.reply_token, template_message)


    #如果Confirm收到45(Corridor的最後一題)的話要跳回去Ct
    elif extract(event.postback.data) == 45:#絕對題數
        ct_container = []
        ct_container.append(Corridor2)

        if data[userid]['Normal'] == 12:#該類題數
            ct_container.append(Normal2)
        else:
            ct_container.append(Normal1)

        if data[userid]['Indoors'] == 20:#該類題數
            ct_container.append(Indoors2)
        else:
            ct_container.append(Indoors1)

        if data[userid]['Outdoors'] == 19:#該類題數
            ct_container.append(Outdoors2)
        else:
            ct_container.append(Outdoors1)

        carousel_template = CarouselTemplate(columns=ct_container)
        template_message = TemplateSendMessage(alt_text='問卷選單', template=carousel_template)
        #把CT推出去
        line_bot_api.reply_message(
            event.reply_token, template_message)


    #如果Confirm收到64(Outdoors的最後一題)的話要跳回去Ct
    elif extract(event.postback.data) == 64:#絕對題數
        ct_container = []
        ct_container.append(Outdoors2)

        if data[userid]['Normal'] == 12:#該類題數
            ct_container.append(Normal2)
        else:
            ct_container.append(Normal1)

        if data[userid]['Indoors'] == 20:#該類題數
            ct_container.append(Indoors2)
        else:
            ct_container.append(Indoors1)

        if data[userid]['Corridor'] == 13:#該類題數
            ct_container.append(Corridor2)
        else:
            ct_container.append(Corridor1)

        carousel_template = CarouselTemplate(columns=ct_container)
        template_message = TemplateSendMessage(alt_text='問卷選單', template=carousel_template)
        #把CT推出去
        line_bot_api.reply_message(
            event.reply_token, template_message)
