import pandas as pd
import sqlite3

#DB開關
conn = sqlite3.connect('diana.db')
c = conn.cursor()
#讀csv
data = pd.read_csv("question.csv")
#建question表格
c.execute("CREATE TABLE IF NOT EXISTS question (no integer, content text, category text);")


for i in range(len(data)):
    no = data["no"][i]
    content = data["content"][i]
    category = data["category"][i]

    #寫入資料庫
    c.execute('INSERT INTO question VALUES ({},"{}","{}");'.format(no, content, category))
    conn.commit()


conn.close