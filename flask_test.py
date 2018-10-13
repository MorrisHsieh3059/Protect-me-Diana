from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi("apQkyD5cnxa8kanS8yfnr+ExfDR/yUoKmLXVu7epNzWsXqIoD1twn/YCGRnhIZLv4r36JYsjzVlpfWMHHaoTs9V4d/somxpkAI0ZNpiG8axYMp+xMbVvcC5vwyKEGizJWZ4CK1KX5DFqVxe5mb5lPgdB04t89/1O/w1cDnyilFU=
")
handler = WebhookHandler("e1af475f2498d7d75ecceca445f69bf7
")


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
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
