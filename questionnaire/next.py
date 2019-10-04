from linebot.models import (
    TextSendMessage,
)

from .confirm import confirm    #抓confirm template 進來

def next(data, userid, parse, db):
    cat = parse[0]
    Q = parse[1]

    if Q in data[userid]["Answered"][cat]:
        return TextSendMessage(text="您已經填寫過此題了！請填頁面上的最後一題"), "00"

    else:
        if parse[2] == 'OK':
            data[userid]["Answered"][cat].append(Q)
            return confirm(cat, Q, db), "00"

        elif parse[2] == 'NO':
            data[userid]["cat"] = cat
            data[userid]["Q"] = Q
            return TextSendMessage(text="請簡述災情"), "01"

    # 功能：首先，不讓他重複填答。若使用者回覆沒問題，則在data[userid]['Answered']中
    #      加入該題絕對題號，然後計數器data[userid][cat] + 1，並且推下議題的confirm
    #      template；若該題之回覆為待改進，則叫他打字
    # 輸入：
    #      1. data
    #      2. userid
    #      3. cat
    #      4. parse:extarct(event.postback.data) [0]是絕對題號；[1]是OK/NO
    # 輸出：
    #      0. (str) 叫他不要重複填寫
    #      1. 沒問題：ConfirmTemplate & result = True
    #      2. 待改進：(str)叫他簡述災情 & result = False
