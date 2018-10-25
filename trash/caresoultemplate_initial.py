


from __future__ import unicode_literals

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton)

from linebot.models import TemplateSendMessage, CarouselTemplate, CarouselColumn, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction



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
