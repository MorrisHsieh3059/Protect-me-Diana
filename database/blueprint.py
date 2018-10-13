import sqlite3
conn = sqlite3.connect('diana.db')
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS question (no integer, content text, category text);")
