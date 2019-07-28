import re

def extract(x):
    y = re.findall("no=([^&]+)", x)
    a = re.findall("wer=([^&]+)", x)
    b = a[0]
    z = y[0]
    z = int(z)
    e = [z, b]

    return e

    # 功能：把confirm template的event.postback.data擷取出絕對題號、回應
    # 輸入：event.postback.data (即Line吃到的PostbackEvent)
    #                          EX:'no=' + str(questions[i][0]) + '&answer=OK'
    #                          EX:'no=' + str(questions[i][0]) + '&answer=NO'
    # 輸出：list(['絕對題號', 'OK/NO(沒問題或待改進)'])

def revise_extract(text):

    cat = text[0]
    i = int(text[1:])

    cat = 'Quick' if cat == 'Q' or cat =='q' else cat
    cat = 'Normal' if cat == 'N' or cat =='n' else cat
    cat = 'Indoors' if cat == 'I' or cat =='i' else cat
    cat = 'Corridor' if cat == 'C' or cat =='c' else cat
    cat = 'Outdoors' if cat == 'O' or cat =='o' else cat

    lst = [cat, i]



    return lst

    # 功能：把使用者在回答要修改表單答覆之後，我們要把他輸入的文字訊息，抓出類別、題號
    # 輸入：str (即Line吃到的text)
    #          EX:'Normal Q17'
    # 輸出：list(['類別', '相對題號'])
