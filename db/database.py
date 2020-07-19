import sqlite3
import psycopg2
from psycopg2 import sql

from questionnaire.converter import converter

class Database:
    def __init__(self, info_str, db_type='sqlite3'):
        self.conn = None
        self.db_type = db_type

        if db_type == 'sqlite3':
            self.conn = sqlite3.connect(info_str)
        elif db_type == 'postgres':
            self.conn = psycopg2.connect(info_str)
        else:
            raise ValueError('Invalid `db_type`: ' + db_type)

    def __del__(self):
        self.conn.close()

    def get_building_id(self, name):
        cur = self.conn.cursor()
        cur.execute("""select * FROM buildings WHERE name = '%s'""" % (name))
        ret = cur.fetchall()
        print(ret)
        return ret

    """ questionnaire.get_res_db.py """
    def get_feedback(self, feedback, userid, b_id):
        #DB開關
        cur = self.conn.cursor()

        #建response表格
        cur.execute("""CREATE TABLE IF NOT EXISTS responses (
                YN integer,
                description text,
                contact_id text,
                time timestamp default current_timestamp,
                question_id integer,
                assessment_id integer default 0,
                building_id text,
                position text,
                img_url text,
                room text);""")

        a = {i: None for i in range(1, 78)}
        for cat, q, value, pos, img_url, build, room in feedback:
            i = converter(cat, q)
            a[i] = [value, pos, img_url, build, room]

        assessment_id = self.get_latest_assessment_id_db()[0]
        body = []

        for i, value in a.items():
            yn = value is None
            if value is not None:
                body.append((yn, value[0], userid, i, assessment_id, value[1], value[2], value[3], value[4]))
            else:
                body.append((yn, None, userid, i, assessment_id, None, None, b_id, None))

        sql = self.sql
        if sql:
            query = sql.SQL('INSERT INTO responses (YN, description, contact_id, question_id, assessment_id, position, img_url, building_id, room) VALUES {};').format(
                sql.SQL(', ').join([
                    sql.SQL('({})').format(sql.SQL(', ').join([sql.Literal(c) for c in row]))
                    for row in body
                ]),
            )
            cur.execute(query)
        else:
            cur.executemany('INSERT INTO responses (YN, description, contact_id, question_id, assessment_id) VALUES (%s, %s, %s, %s, %s);', body)

        self.conn.commit()
        cur.close()

    """ assessment.get_latest_assessment_id_db.py """
    def get_latest_assessment_id_db(self):
        cur = self.conn.cursor()
        cur.execute("""SELECT * FROM assessments""")
        result = cur.fetchall()
        if len(result) > 0:
            ret = result[len(result) - 1]
        else:
            print("No Event!")
            return
        self.conn.commit()
        cur.close()
        return ret

    """ questionnaire.get_question_db.py """
    def get_category(self, cat):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM question WHERE category=%s;", (cat, ))
        ret = cur.fetchall()
        cur.close()
        return ret

    def get_all(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM question;")
        ret = cur.fetchall()
        cur.close()
        return ret

    """ questionnaire.get_yitianda_db.py """
    def get_yitianda_db(self, ass_id = None):
        if ass_id == None:
            ass_id = self.get_latest_assessment_id_db()[0]

        cur = self.conn.cursor()
        cur.execute('SELECT * FROM responses WHERE assessment_id=%s ', (ass_id,))
        response = cur.fetchall()

        # 整理出以填答過的人，放進一個list
        yitianda = []
        for i in range(len(response)):
            userid = response[i][2]
            if userid not in yitianda:
                yitianda.append(userid)

        self.conn.commit()
        cur.close()

        ### Remove developmer
        develeoper = [
                      'Uf06239f6f01f24d5664045d8333ab49d',
                      'Ude4a997b36abb3659976a7605f1292a7',
                      'Ue9b74fc6a04d98213c2f4a413c0dd71c',
                      'U4f1e3cfe2a200dc510fcd4762810e485',
                      'Ud63abdec42ee4c3a902c8ef5a32b1c9f',
                      'U26256bf9c95da598df3978e9b37c4d1d',
                      'U1389969c0ba7fd6213c87d2d90d508c9',
                     ]

        for dev in develeoper:
            if dev in yitianda:
                yitianda.remove(dev)

        print(f"\n=================\nGet yitianda users:\n{yitianda}\n===================")

        return yitianda

    @property
    def sql(self):
        if self.db_type == 'postgres':
            return sql
        else:
            return None
