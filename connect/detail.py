import ast

def detail(payload, db):
    payload = ast.literal_eval(payload)
    # UID = payload["userid"]
    assessment_id = payload["assessment_id"]
    building_id = payload["building_id"]
    detail = {}

    cur = db.conn.cursor()
    cur.execute(
        """SELECT b.name AS building, q.category AS category, q.num AS question,
                  q.content AS content, r.description AS description,
                  r.img_url AS img_url, r.position AS position, q.id AS abs_q
           FROM questions AS q
           JOIN responses AS r
              ON r.question_id = q.id
           JOIN buildings AS b
              ON b.id = r.building_id
           WHERE (yn IS FALSE AND building_id = %s AND assessment_id = %s);""",
        (building_id, assessment_id),
    )

    #yn 是 responses 裡面的待改進
    ret = cur.fetchall()
    db.conn.commit()
    for i in range(len(ret)):
        per = ret[i]
        detail[per[7]] = {
            "question": per[1] + " Q" + str(per[2]),
            "content": per[3],
            "description": per[4],
            "img_url": per[5],
            "pos": per[6],
        }

    db.conn.commit()
    cur.close()
    return detail
