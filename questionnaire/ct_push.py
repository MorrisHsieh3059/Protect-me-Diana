from .carousel import *          #CT抓欄位

def ct_push(data, userid, quick, status, db):
    ct_container = []

    # if data[userid] == { "Answered": { "Quick": [], "Normal":[], "Indoors":[], "Corridor":[], "Outdoors":[] }, "status": "pre-class", "feedback": [], "current": (), "building": ""} and quick == 0:
    if data[userid]["Answered"] == { "Quick": [], "Normal":[], "Indoors":[], "Corridor":[], "Outdoors":[] } and data[userid]["status"] == "pre-class" and data[userid]["feedback"] == [] and data[userid]["current"] == () and quick == 0:
        ct_container = [Quick, Standard]

    else:

        if len(db.get_category('Normal')) - 1 in data[userid]['Answered']['Normal'] and status == 1:#該類題數
            ct_container.insert(0, Normal1)
        else:
            ct_container.insert(0, Normal0)

        if len(db.get_category('Indoors')) - 1 in data[userid]['Answered']['Indoors'] and status == 1:#該類題數
            ct_container.insert(1, Indoors1)
        else:
            ct_container.insert(1, Indoors0)

        if len(db.get_category('Corridor')) - 1 in data[userid]['Answered']['Corridor'] and status == 1:#該類題數
            ct_container.insert(2, Corridor1)
        else:
            ct_container.insert(2, Corridor0)

        if len(db.get_category('Outdoors')) - 1 in data[userid]['Answered']['Outdoors'] and status == 1:#該類題數
            ct_container.insert(3, Outdoors1)
        else:
            ct_container.insert(3, Outdoors0)

        if data[userid]['Answered']['Quick'] == [] and data[userid]['Answered']['Normal'] == [] and data[userid]['Answered']['Indoors'] == [] and data[userid]['Answered']['Corridor'] == [] and data[userid]['Answered']['Outdoors'] == [] and quick == 0:
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
