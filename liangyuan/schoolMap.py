import requests
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage, TemplateSendMessage, ConfirmTemplate, MessageTemplateAction, ButtonsTemplate, PostbackTemplateAction, URITemplateAction, CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn, ImageSendMessage, StickerSendMessage, LocationSendMessage, QuickReply, QuickReplyButton, MessageAction, FollowEvent, ImagemapSendMessage, BaseSize, MessageImagemapAction, URIImagemapAction, ImagemapArea, DatetimePickerTemplateAction

def toCheckKey(event, line_bot_api):
    try:
        mtext = event.message.text
        if mtext == '學校區塊01':
            schoolLayout01(event, line_bot_api)

        elif mtext == '學校區塊02':
            schoolLayout02(event, line_bot_api)

        elif mtext == '學校區塊03':
            schoolLayout03(event, line_bot_api)

        elif mtext == '學校區塊04':
            schoolLayout04(event, line_bot_api)

        elif mtext == '學校區塊05':
            schoolLayout05(event, line_bot_api)

        elif mtext == '學校區塊06':
            schoolLayout06(event, line_bot_api)

        elif mtext == '學校區塊07':
            schoolLayout07(event, line_bot_api)

        elif mtext == '學校區塊08':
            schoolLayout08(event, line_bot_api)

        elif mtext == '學校區塊09':
            schoolLayout09(event, line_bot_api)

        elif mtext == '上一頁':
            schoolLayoutPrev(event, line_bot_api)

        elif mtext == '下一頁':
            schoolLayoutNext(event, line_bot_api)

        elif mtext == '回首頁':
            schoolLayout00(event, line_bot_api)

        else:
            userId = event.source.user_id
            line_bot_api.link_rich_menu_to_user(
                userId, 'richmenu-0240ad645743fd684438bf3d66606b79')

    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！toCheckKey'))

# 學校平面圖主選單(標註有9個區塊)；每個區塊選單的回首頁


def schoolLayout00(event, line_bot_api):
    # try:
    userId = event.source.user_id
    message = [
        TextSendMessage(text='請開啟主選單後，選擇要檢查的區塊~'),
        TextSendMessage(text='如要退出，請輸入『000』')
    ]
    line_bot_api.link_rich_menu_to_user(
        userId, 'richmenu-f9f2e62cedbcf5cefa77e31d89aced35')
    line_bot_api.reply_message(event.reply_token, message)
    # except:
    #     line_bot_api.reply_message(
    #         event.reply_token, TextSendMessage(text='發生錯誤！schoolLayout00'))


def schoolLayout01(event, line_bot_api):
    try:
        userId = event.source.user_id
        message = TextSendMessage(text='請選擇要檢查的建物')
        line_bot_api.link_rich_menu_to_user(
            userId, 'richmenu-b10d61385214045c56a13055a0b9f3a9')
        line_bot_api.reply_message(event.reply_token, message)

    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！schoolLayout01'))


def schoolLayout02(event, line_bot_api):
    try:
        userId = event.source.user_id
        message = TextSendMessage(text='請選擇要檢查的建物')
        line_bot_api.link_rich_menu_to_user(
            userId, 'richmenu-88b9ad4ad42288cd301cf35925f3d7c8')
        line_bot_api.reply_message(event.reply_token, message)

    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！schoolLayout02'))


def schoolLayout03(event, line_bot_api):
    try:
        userId = event.source.user_id
        message = TextSendMessage(text='請選擇要檢查的建物')
        line_bot_api.link_rich_menu_to_user(
            userId, 'richmenu-0fc92f8640d831b3159ebcdd62ee1ce3')
        line_bot_api.reply_message(event.reply_token, message)

    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！schoolLayout03'))


def schoolLayout04(event, line_bot_api):
    try:
        userId = event.source.user_id
        message = TextSendMessage(text='請選擇要檢查的建物')
        line_bot_api.link_rich_menu_to_user(
            userId, 'richmenu-34f7511662abc8adb612899b9f8c639a')
        line_bot_api.reply_message(event.reply_token, message)

    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！schoolLayout04'))


def schoolLayout05(event, line_bot_api):
    try:
        userId = event.source.user_id
        message = TextSendMessage(text='請選擇要檢查的建物')
        line_bot_api.link_rich_menu_to_user(
            userId, 'richmenu-a60905df9fa2705d972b805aeb0b70df')
        line_bot_api.reply_message(event.reply_token, message)

    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！schoolLayout05'))


def schoolLayout06(event, line_bot_api):
    try:
        userId = event.source.user_id
        message = TextSendMessage(text='請選擇要檢查的建物')
        line_bot_api.link_rich_menu_to_user(
            userId, 'richmenu-fa55218c41ab03a82de79fe321be875e')
        line_bot_api.reply_message(event.reply_token, message)

    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！schoolLayout06'))


def schoolLayout07(event, line_bot_api):
    try:
        userId = event.source.user_id
        message = TextSendMessage(text='請選擇要檢查的建物')
        line_bot_api.link_rich_menu_to_user(
            userId, 'richmenu-b933fec3e3de3e92bb271e805d8f473f')
        line_bot_api.reply_message(event.reply_token, message)

    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！schoolLayout07'))


def schoolLayout08(event, line_bot_api):
    try:
        userId = event.source.user_id
        message = TextSendMessage(text='請選擇要檢查的建物')
        line_bot_api.link_rich_menu_to_user(
            userId, 'richmenu-2e19234a741692098e3972ba4bd34451')
        line_bot_api.reply_message(event.reply_token, message)

    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！schoolLayout08'))


def schoolLayout09(event, line_bot_api):
    try:
        userId = event.source.user_id
        message = TextSendMessage(text='請選擇要檢查的建物')
        line_bot_api.link_rich_menu_to_user(
            userId, 'richmenu-ff85972065979651bcced6a651e554af')
        line_bot_api.reply_message(event.reply_token, message)

    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！schoolLayout09'))

# 每個區塊選單的上一頁


def schoolLayoutPrev(event, line_bot_api):
    try:
        userId = event.source.user_id
        rich_menu_id = line_bot_api.get_rich_menu_id_of_user(userId)
        message = TextSendMessage(text='請選擇要檢查的建物')
        if rich_menu_id == 'richmenu-88b9ad4ad42288cd301cf35925f3d7c8':
            line_bot_api.link_rich_menu_to_user(
                userId, 'richmenu-b10d61385214045c56a13055a0b9f3a9')
        elif rich_menu_id == 'richmenu-0fc92f8640d831b3159ebcdd62ee1ce3':
            line_bot_api.link_rich_menu_to_user(
                userId, 'richmenu-88b9ad4ad42288cd301cf35925f3d7c8')
        elif rich_menu_id == 'richmenu-34f7511662abc8adb612899b9f8c639a':
            line_bot_api.link_rich_menu_to_user(
                userId, 'richmenu-0fc92f8640d831b3159ebcdd62ee1ce3')
        elif rich_menu_id == 'richmenu-a60905df9fa2705d972b805aeb0b70df':
            line_bot_api.link_rich_menu_to_user(
                userId, 'richmenu-34f7511662abc8adb612899b9f8c639a')
        elif rich_menu_id == 'richmenu-fa55218c41ab03a82de79fe321be875e':
            line_bot_api.link_rich_menu_to_user(
                userId, 'richmenu-a60905df9fa2705d972b805aeb0b70df')
        elif rich_menu_id == 'richmenu-b933fec3e3de3e92bb271e805d8f473f':
            line_bot_api.link_rich_menu_to_user(
                userId, 'richmenu-fa55218c41ab03a82de79fe321be875e')
        elif rich_menu_id == 'richmenu-2e19234a741692098e3972ba4bd34451':
            line_bot_api.link_rich_menu_to_user(
                userId, 'richmenu-b933fec3e3de3e92bb271e805d8f473f')
        elif rich_menu_id == 'richmenu-ff85972065979651bcced6a651e554af':
            line_bot_api.link_rich_menu_to_user(
                userId, 'richmenu-2e19234a741692098e3972ba4bd34451')
        else:
            line_bot_api.link_rich_menu_to_user(
                userId, 'richmenu-f9f2e62cedbcf5cefa77e31d89aced35')
            message = [
                TextSendMessage(text='請選擇要檢查的區塊'),
                TextSendMessage(text='如要退出，請輸入『000』')
            ]

        line_bot_api.reply_message(event.reply_token, message)

    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！schoolLayoutPrev'))

# 每個區塊選單的下一頁


def schoolLayoutNext(event, line_bot_api):
    try:
        userId = event.source.user_id
        rich_menu_id = line_bot_api.get_rich_menu_id_of_user(userId)
        message = TextSendMessage(text='請選擇要檢查的建物')
        if rich_menu_id == 'richmenu-b10d61385214045c56a13055a0b9f3a9':
            line_bot_api.link_rich_menu_to_user(
                userId, 'richmenu-88b9ad4ad42288cd301cf35925f3d7c8')
        elif rich_menu_id == 'richmenu-88b9ad4ad42288cd301cf35925f3d7c8':
            line_bot_api.link_rich_menu_to_user(
                userId, 'richmenu-0fc92f8640d831b3159ebcdd62ee1ce3')
        elif rich_menu_id == 'richmenu-0fc92f8640d831b3159ebcdd62ee1ce3':
            line_bot_api.link_rich_menu_to_user(
                userId, 'richmenu-34f7511662abc8adb612899b9f8c639a')
        elif rich_menu_id == 'richmenu-34f7511662abc8adb612899b9f8c639a':
            line_bot_api.link_rich_menu_to_user(
                userId, 'richmenu-a60905df9fa2705d972b805aeb0b70df')
        elif rich_menu_id == 'richmenu-a60905df9fa2705d972b805aeb0b70df':
            line_bot_api.link_rich_menu_to_user(
                userId, 'richmenu-fa55218c41ab03a82de79fe321be875e')
        elif rich_menu_id == 'richmenu-fa55218c41ab03a82de79fe321be875e':
            line_bot_api.link_rich_menu_to_user(
                userId, 'richmenu-b933fec3e3de3e92bb271e805d8f473f')
        elif rich_menu_id == 'richmenu-b933fec3e3de3e92bb271e805d8f473f':
            line_bot_api.link_rich_menu_to_user(
                userId, 'richmenu-2e19234a741692098e3972ba4bd34451')
        elif rich_menu_id == 'richmenu-2e19234a741692098e3972ba4bd34451':
            line_bot_api.link_rich_menu_to_user(
                userId, 'richmenu-ff85972065979651bcced6a651e554af')
        else:
            line_bot_api.link_rich_menu_to_user(
                userId, 'richmenu-f9f2e62cedbcf5cefa77e31d89aced35')
            message = [
                TextSendMessage(text='請選擇要檢查的區塊'),
                TextSendMessage(text='如要退出，請輸入『000』')
            ]

        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！schoolLayoutNext'))
