from linebot import (
    LineBotApi, WebhookHandler
)

line_bot_api = LineBotApi("apQkyD5cnxa8kanS8yfnr+ExfDR/yUoKmLXVu7epNzWsXqIoD1twn/YCGRnhIZLv4r36JYsjzVlpfWMHHaoTs9V4d/somxpkAI0ZNpiG8axYMp+xMbVvcC5vwyKEGizJWZ4CK1KX5DFqVxe5mb5lPgdB04t89/1O/w1cDnyilFU=", "http://localhost:8080")
handler = WebhookHandler("e1af475f2498d7d75ecceca445f69bf7")
