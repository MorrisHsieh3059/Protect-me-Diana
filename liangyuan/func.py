import os

from linebot import LineBotApi, WebhookHandler
# from linebot.models import TextSendMessage, TemplateSendMessage, ConfirmTemplate, MessageTemplateAction, ButtonsTemplate, PostbackTemplateAction, URITemplateAction, CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn, ImageSendMessage, StickerSendMessage, LocationSendMessage, QuickReply, QuickReplyButton, MessageAction, FollowEvent
from linebot.models import *
from . import schoolMap, floorMap, classroomMap

if os.environ.get("FLASK_ENV") == "development":
    line_bot_api = LineBotApi(os.environ.get("TOKEN"), "http://localhost:8080")
else:
    line_bot_api = LineBotApi(os.environ.get("TOKEN"))

handler = WebhookHandler(os.environ.get("SECRET"))

# 主選單功能
def toCheck(event, line_bot_api):
    """
        以後想改成的流程
            1. 丟校園平面圖、切成各區塊 ==> 客製化
            2. 丟局部校園圖、標明各大樓 ==> 客製化
                throw signal ==> 需要記錄大樓名字
            3. 叫使用者選樓層 ==> 客製化
            4. 丟樓層平面圖 ==> 客製化
                throw signal ==> 需要記錄教室名字
            -- Module 1 end--
    """
    # try:
    mtext = event.message.text
    if mtext == '請給我表單填寫':
        toInspection(event)
        return "pre", ""

    elif mtext == '紀錄':
        toRecord(event)
        return "pre", ""

    elif mtext == '使用指南':
        toUserGuide(event)
        return "pre", ""

    elif mtext == '通知':
        toInform(event)
        return "pre", ""

    elif mtext == '設定':
        toSetting(event)
        return "pre", ""

    elif mtext == '相關資源':
        toResource(event)
        return "pre", ""

    elif mtext == '災後自主檢查':                 ### core porcess
        afterDisasterAutonomousCheck(event, line_bot_api)
        return "pre", ""

    elif mtext == '災後通報檢查':                 ### skip
        postDisasterNotificationCheck(event)
        return "pre", ""

    elif mtext == '年度例行檢查':                 ### skip
        annualRoutineCheck(event)
        return "pre", ""

    elif mtext == '災防模擬檢查':                 ### skip
        disasterPreventionSimulationCheck(event)
        return "pre", ""

    elif '學校區塊' in mtext:
        schoolMap.toCheckKey(event, line_bot_api)
        return "pre", ""

    elif mtext == '上一頁':
        schoolMap.toCheckKey(event, line_bot_api)
        return "pre", ""

    elif mtext == '下一頁':
        schoolMap.toCheckKey(event, line_bot_api)
        return "pre", ""

    elif mtext == '回首頁':
        schoolMap.toCheckKey(event, line_bot_api)
        return "pre", ""

    elif mtext == 'E2工程二館':
        floorMap.sendE2Floor(event, line_bot_api)
        return "pre", "363102-9"

    elif mtext == 'E2-4F':
        classroomMap.send_E2_4F_classroom(event, line_bot_api) ## confirm template
        return "pre", ""

    elif mtext == '東側':
        classroomMap.send_E2_4F_East_classroom(event, line_bot_api)
        return "pre-class", ""

    elif mtext == '000':
        zeroFunc(event)
        return "pre", ""

    ## NTU
    elif mtext == '123':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='請輸入『456』確認'))
        return "pre", "363101-1"

    elif mtext == "456":
        return "pre-class", ""

    else:
        sendMulti(event)
        return "pre", ""

    # except:
    #     line_bot_api.reply_message(
    #         event.reply_token, TextSendMessage(text='發生錯誤！toCheck'))
    #     line_bot_api.unlink_rich_menu_from_user(event.source.user_id)

def zeroFunc(event):
    try:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='已退出操作，謝謝！'))
        userId = event.source.user_id
        line_bot_api.link_rich_menu_to_user(
            userId, 'richmenu-0240ad645743fd684438bf3d66606b79')

    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！zero_func'))
        line_bot_api.unlink_rich_menu_from_user(event.source.user_id)

def sendMulti(event):  # 多項傳送
    try:
        message = [  # 串列
            StickerSendMessage(  # 傳送貼圖
                package_id='11537',
                sticker_id='52002738'
            ),
            TextSendMessage(  # 傳送文字
                text="請用主選單來操作唷~"
            ),
        ]
        line_bot_api.reply_message(event.reply_token, message)
        line_bot_api.unlink_rich_menu_from_user(event.source.user_id)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！sendMulti'))

def toInspection(event):  # 檢查
    try:
        message = TextSendMessage(
            text='請選擇檢查的類型',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        image_url='https://i.imgur.com/jVXSmnY.png?size=30',
                        action=MessageAction(label="災後自主檢查", text="災後自主檢查")
                    ),
                    QuickReplyButton(
                        image_url='https://i.imgur.com/KuvpMya.png?size=30',
                        action=MessageAction(label="災後通報檢查", text="災後通報檢查")
                    ),
                    QuickReplyButton(
                        image_url='https://i.imgur.com/9o0d3qQ.png?size=30',
                        action=MessageAction(label="年度例行檢查", text="年度例行檢查")
                    ),
                    QuickReplyButton(
                        image_url='https://i.imgur.com/vEL2MNm.png?size=30',
                        action=MessageAction(label="災防模擬檢查", text="災防模擬檢查")
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！toInspection'))

def afterDisasterAutonomousCheck(event, line_bot_api):  # 災後自主檢查
    # try:
    schoolMap.schoolLayout00(event, line_bot_api)
    # except:
    #     line_bot_api.reply_message(event.reply_token, TextSendMessage(
    #         text='發生錯誤！afterDisasterAutonomousCheck'))

def postDisasterNotificationCheck(event):  # 災後通報檢查
    try:
        sendMulti(event)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            text='發生錯誤！postDisasterNotificationCheck'))

def annualRoutineCheck(event):  # 年度例行檢查
    try:
        sendMulti(event)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！annualRoutineCheck'))

def disasterPreventionSimulationCheck(event):  # 災防模擬檢查
    try:
        sendMulti(event)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            text='發生錯誤！disasterPreventionSimulationCheck'))

def toRecord(event):  # 紀錄
    try:
        message = [
            TextSendMessage(  # 傳送文字
                text="請選擇檢查的類型"
            ),
            TemplateSendMessage(
                alt_text='圖片旋轉選單',
                template=ImageCarouselTemplate(
                    columns=[
                        ImageCarouselColumn(
                            image_url='https://i.imgur.com/G1LRdkh.png?size=200',
                            action=MessageTemplateAction(
                                label='災後自主檢查',
                                text='災後自主檢查'
                            )
                        ),
                        ImageCarouselColumn(
                            image_url='https://i.imgur.com/LK1BxcH.png?size=200',
                            action=MessageTemplateAction(
                                label='災後通報檢查',
                                text='災後通報檢查'
                            )
                        ),
                        ImageCarouselColumn(
                            image_url='https://i.imgur.com/dzmWPIw.png?size=200',
                            action=MessageTemplateAction(
                                label='年度例行檢查',
                                text='年度例行檢查'
                            )
                        ),
                        ImageCarouselColumn(
                            image_url='https://i.imgur.com/rICqk0c.png?size=200',
                            action=MessageTemplateAction(
                                label='災防模擬檢查',
                                text='災防模擬檢查'
                            )
                        )
                    ]
                )
            )
        ]
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！toRecord'))

def toUserGuide(event):  # 使用指南
    try:
        sendMulti(event)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！toUserGuide'))

def toInform(event):  # 通知
    try:
        message = TextSendMessage(
            text='請選擇檢查的類型',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="災後自主檢查", text="災後自主檢查")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="災後通報檢查", text="災後通報檢查")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="年度例行檢查", text="年度例行檢查")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="災防模擬檢查", text="災防模擬檢查")
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！toInform'))

def toSetting(event):  # 設定
    try:
        message = TextSendMessage(
            text='請選擇檢查的類型',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="災後自主檢查", text="災後自主檢查")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="災後通報檢查", text="災後通報檢查")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="年度例行檢查", text="年度例行檢查")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="災防模擬檢查", text="災防模擬檢查")
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！toSetting'))

def toResource(event):  # 相關資源
    try:
        message = TextSendMessage(
            text='請選擇檢查的類型',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="災後自主檢查", text="災後自主檢查")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="災後通報檢查", text="災後通報檢查")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="年度例行檢查", text="年度例行檢查")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="災防模擬檢查", text="災防模擬檢查")
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！toResource'))

def sendText(event):  # 傳送文字
    try:
        message = TextSendMessage(
            text="我是 Linebot，\n您好！"
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！sendText'))

def sendImage(event):  # 傳送圖片
    try:
        message = ImageSendMessage(
            original_content_url="https://i.imgur.com/4QfKuz1.png",
            preview_image_url="https://i.imgur.com/4QfKuz1.png"
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！sendImage'))

def sendStick(event):  # 傳送貼圖
    try:
        message = StickerSendMessage(  # 貼圖兩個id需查表
            package_id='1',
            sticker_id='2'
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！sendStick'))

def sendPosition(event):  # 傳送位置
    try:
        message = LocationSendMessage(
            title='101大樓',
            address='台北市信義路五段7號',
            latitude=25.034207,  # 緯度
            longitude=121.564590  # 經度
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！sendPosition'))

def sendQuickreply(event):  # 快速選單
    try:
        message = TextSendMessage(
            text='請選擇最喜歡的程式語言',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="Python", text="Python")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="Java", text="Java")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="C#", text="C#")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="Basic", text="Basic")
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！sendQuickreply'))

def toNull(event):
    try:
        message = TextSendMessage(text='請輸入資料或是想進行的操作，\n謝謝！')
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！toNull'))
