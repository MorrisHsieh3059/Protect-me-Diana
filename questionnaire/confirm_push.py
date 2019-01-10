from linebot.models import (
    TextSendMessage,
)

from .confirm import confirm            #抓confirm template 進來


def confirm_push(data, userid, cat, db):

        if data[userid]['Quick'] != 0:#QC填到一半 智障又打一次carousel
            return TextSendMessage(text="您已選擇快速檢核！請填頁面上的最後一題")

        elif data[userid]['Normal'] != 0 or data[userid]['Indoors'] != 0 or data[userid]['Corridor'] != 0 or data[userid]['Outdoors'] != 0:
            if cat == 'Quick': #不讓她劈腿(換成QC)
                 return TextSendMessage(text="您已選擇正規問卷！請填頁面上的最後一題")
            else:
                return confirm(cat ,data[userid][cat], db)

        else:
            return confirm(cat ,data[userid][cat], db)

    # 功能： 回傳confirm template
    #       條件───1. 不讓他填Quick Check填到一半換類別
    #             2.  不讓他從後面四項類別，喚回Quick Check
    # 輸入： 1. data  ：使用者填答紀錄
    #       2. userid ：使用者的ID
    #       3. cat    ：使用者現在填到的類別
    # 輸出： confirm (一個函數 -- 請見下回分曉)
