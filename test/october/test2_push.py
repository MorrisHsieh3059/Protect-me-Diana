from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage
from linebot.exceptions import LineBotApiError

CHANNEL_ACCESS_TOKEN = "apQkyD5cnxa8kanS8yfnr+ExfDR/yUoKmLXVu7epNzWsXqIoD1twn/YCGRnhIZLv4r36JYsjzVlpfWMHHaoTs9V4d/somxpkAI0ZNpiG8axYMp+xMbVvcC5vwyKEGizJWZ4CK1KX5DFqVxe5mb5lPgdB04t89/1O/w1cDnyilFU="


toM = "Uf06239f6f01f24d5664045d8333ab49d"
#Bourbon
toB = "Ue9b74fc6a04d98213c2f4a413c0dd71c"
#Wayne
toW = "Ude4a997b36abb3659976a7605f1292a7"


line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

#文字訊息


try:
    line_bot_api.push_message(to0, TextSendMessage(text='帥哞怎麼這麼帥'))
    line_bot_api.push_message(to1, TextSendMessage(text='帥哞怎麼這麼帥'))
    line_bot_api.push_message(to2, TextSendMessage(text='小魚你欠揍是不是'))
except LineBotApiError as e:
    # error handle
    raise e

#圖片訊息
# ImageSendMessage物件中的輸入
# original_content_url 以及 preview_image_url都要寫才不會報錯。
#輸入的網址要是一個圖片，應該說只能是一個圖片，不然不會報錯但是傳過去是灰色不能用的圖
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
image_url = "https://i.imgur.com/eTldj2E.png?1"
try:
    line_bot_api.push_message(to, ImageSendMessage(original_content_url=image_url, preview_image_url=image_url))
except LineBotApiError as e:
    # error handle
    raise e
