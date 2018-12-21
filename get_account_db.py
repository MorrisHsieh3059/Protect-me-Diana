import sqlite3

def get_account_db(account):

    conn = sqlite3.connect('diana.db')
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS contacts (line_userid text, name text, county text, school text, phone text);")

    line_userid = account["userid"]
    name = account["name"]
    county = account["county"]
    school = account["school"]
    phone = account["phone"]

    #寫入資料庫
    c.execute('INSERT INTO contacts VALUES ("{}","{}","{}","{}","{}");'.format(line_userid, name, county, school, phone))
    conn.commit()
    conn.close()

    ##################################
    ##########找所有人的userid#########
    ##################################

def get_userid_db():

    conn = sqlite3.connect('diana.db')
    c = conn.cursor()

    cursor = c.execute('SELECT * FROM contacts')

    result = cursor.fetchall()
    userid = []

    for i in range(len(result)):
        uid = result[i][0]
        userid.append(uid)

    conn.commit()
    conn.close()

    return userid

    ##################################
    ##########刪掉重複的userid#########
    ##################################

def delete_userid_db(userid):

    conn = sqlite3.connect('diana.db')
    c = conn.cursor()

    c.execute("DELETE from contacts WHERE line_userid='{}'".format(userid))

    conn.commit()
    conn.close()
