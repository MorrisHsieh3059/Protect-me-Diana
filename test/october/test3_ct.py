
from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage
from linebot.exceptions import LineBotApiError
CHANNEL_ACCESS_TOKEN = "apQkyD5cnxa8kanS8yfnr+ExfDR/yUoKmLXVu7epNzWsXqIoD1twn/YCGRnhIZLv4r36JYsjzVlpfWMHHaoTs9V4d/somxpkAI0ZNpiG8axYMp+xMbVvcC5vwyKEGizJWZ4CK1KX5DFqVxe5mb5lPgdB04t89/1O/w1cDnyilFU="

##Q1_________如何多個to
##Q2_________WHY一次有兩個

#Morris
toM = "Uf06239f6f01f24d5664045d8333ab49d"
#Bourbon
toB = "Ue9b74fc6a04d98213c2f4a413c0dd71c"
#Wayne
toW = "Ude4a997b36abb3659976a7605f1292a7"




#已填答的話 : 建立一個dictionary, 前面裝cat的key, 後面接的value是問題的矩陣(tuple), 然後傳TRUE, False決定田煤田

from linebot.models import TemplateSendMessage, CarouselTemplate, CarouselColumn, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction

image_url_1 = "https://sdl-stickershop.line.naver.jp/stickershop/v1/sticker/60932570/android/sticker.png"
image_url_2 = "https://stickershop.line-scdn.net/stickershop/v1/sticker/11482775/ANDROID/sticker.png"
image_url_3 = "https://stickershop.line-scdn.net/stickershop/v1/product/9601/LINEStorePC/main@2x.png;compress=true"
image_url_4 = "https://sdl-stickershop.line.naver.jp/stickershop/v1/sticker/11482762/android/sticker.png"
image_url_5 = "https://stickershop.line-scdn.net/stickershop/v1/product/1040299/LINEStorePC/main@2x.png;compress=true"


QS = CarouselColumn(
        thumbnail_image_url=image_url_1,
        title='Quick Start',
        text='這是快速檢核喲~',
        actions=[
            PostbackTemplateAction(
                label='開始填寫',
                #text='postback text1',
                data='result=1'
            )
        ]
    )

Normal1 = CarouselColumn(
        thumbnail_image_url=image_url_2,
        title='Normal',
        text='這是一般性檢查',
        actions=[
            PostbackTemplateAction(
                label='開始填寫',
                #text='postback text1',
                data='result=2'
            )
        ]
    )

Normal2 = CarouselColumn(
        thumbnail_image_url=image_url_2,
        title='Normal',
        text='這是一般性檢查',
        actions=[
            PostbackTemplateAction(
                label='已經填寫過了唷',
                #text='postback text1',
                data='result=2'
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
                #text='postback text1',
                data='result=3'
            )
        ]
    )

Indoors2 = CarouselColumn(
        thumbnail_image_url=image_url_3,
        title='Indoors',
        text='這是門/窗/牆/天花板/柱/地板',
        actions=[
            PostbackTemplateAction(
                label='已經填寫過了唷',
                #text='postback text1',
                data='result=3'
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
                #text='postback text2',
                data='result=4'
            )
        ]
    )

Corridor2 = CarouselColumn(
        thumbnail_image_url=image_url_4,
        title='Corridor',
        text='這是欄杆/樓梯/走廊',
        actions=[
            PostbackTemplateAction(
                label='已經填寫過了唷',
                #text='postback text2',
                data='result=4'
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
                #text='postback text2',
                data='result=5'
            )
        ]
    )

Outdoors2 = CarouselColumn(
        thumbnail_image_url=image_url_5,
        title='Outdoors',
        text='這是地基/屋頂/管線/消防',
        actions=[
            PostbackTemplateAction(
                label='已經填寫過了唷',
                #text='postback text2',
                data='result=5'
            )
        ]
    )

carousel_template =CarouselTemplate(
            columns=[QS, Normal1, Normal2, Indoors1, Indoors2, Corridor1, Corridor2, Outdoors1, Outdoors2]
            )
###
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

try:
#   alt_text 因template只能夠在手機上顯示，因此在PC版會使用alt_Text替代
    #line_bot_api.push_message(to, TemplateSendMessage(alt_text="Carousel Template Example", template=carousel_template))
    line_bot_api.push_message(toM, TemplateSendMessage(alt_text="這是謝君模傳的", template = carousel_template ))
    line_bot_api.push_message(toW, TemplateSendMessage(alt_text="這是謝君模傳的", template = carousel_template ))
    line_bot_api.push_message(toB, TemplateSendMessage(alt_text="這是謝君模傳的", template = carousel_template ))

except LineBotApiError as e:
    # error handle
    raise e
