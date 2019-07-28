from .carousel import *          #CT抓欄位

def ct_push(data, userid, quick, status):
    ct_container = []

    if data[userid] == {"Quick":0, "Normal":0, "Indoors":0, "Corridor":0, "Outdoors":0, "Answered":[]} and quick == 0:
        ct_container = [Quick, Standard]
    else:
        if data[userid]['Normal'] == 12 and status == 1:#該類題數
            ct_container.insert(0, Normal1)
        else:
            ct_container.insert(0, Normal0)

        if data[userid]['Indoors'] == 20 and status == 1:#該類題數
            ct_container.insert(1, Indoors1)
        else:
            ct_container.insert(1, Indoors0)

        if data[userid]['Corridor'] == 13 and status == 1:#該類題數
            ct_container.insert(2, Corridor1)
        else:
            ct_container.insert(2, Corridor0)

        if data[userid]['Outdoors'] == 19 and status == 1:#該類題數
            ct_container.insert(3, Outdoors1)
        else:
            ct_container.insert(3, Outdoors0)

        if len(data[userid]['Answered']) == 0 and quick == 0:
            ct_container.insert(0, Quick)
        else:
            pass

    if ct_container == [Normal1, Indoors1, Corridor1, Outdoors1]:
        ct_container = "All cats have already checked!"
    return ct_container

        # 功能： 判斷每一個類別是否已經填答過，決定要推甚麼carousel columns給他
        #       如果沒有填寫過，就把Quick Check加進要推的carousel template
        # 輸入：data, userid, quick, status (1代表該類別確認不修改)
        #                    這個如果是0代表他要填QUICK，1代表詳細
        # 輸出：CarouselTemplate
