import sqlite3

from assessment.get_latest_assessment_id_db import get_latest_assessment_id_db
# 把feedback寫進db

def get_feedback(feedback, userid):
# def get_feedback(feedback, userid, location):
    #DB開關
    conn = sqlite3.connect('response.db') 
    # conn = psycopg2.connect("dbname=pmdianapg user=postgres host=hci.dianalab.net port=10710 password=" + os.environ.get("DBPASSWORD"))

    c = conn.cursor()

    #建response表格
    c.execute("""CREATE TABLE IF NOT EXISTS responses (
            YN integer,
            description text,
            userid text,
            time datetime default current_timestamp,
            question_id integer,
            assessment_id integer default 0,
            building_id integer default 0);""")

    # a = {i:None for i in range(65, 78)} if quick else {i:None for i in range(1, 65)}
    a = {i:None for i in range(1, 78)}

    for i,value in feedback:
        a[i] = value


    assessment_id = get_latest_assessment_id_db()[0]

    for i, value in a.items():
        yn = 1 if value is None else 0
        c.execute('INSERT INTO responses (YN, description, userid, question_id, assessment_id) VALUES (?,?,?,?,?);', (yn, value, userid, i, assessment_id))

    conn.commit()
    conn.close()

    # 功能：把app中的暫時使用者回覆(feedback)，寫進資料庫
    # 輸入：1. feedback:使用者所回覆的待改進內容
    #      2. userid
    #      3. (Bool) quick：看看他是不是填Quick Check，是則T否則F
    # 輸出：寫進response.db
