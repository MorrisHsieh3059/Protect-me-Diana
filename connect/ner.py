import ast
from chat_module.ner.demo import ner_sent

def ner(payload, db):
    payload = ast.literal_eval(payload)
    county = payload["county"]
    assessment_id = payload["assessment_id"]

    cur = db.conn.cursor()
    cur.execute("""SELECT r.description AS description
                    FROM schools AS s
                    JOIN buildings AS b
                       ON s.id = b.school_id
                    JOIN responses AS r
                       ON b.id = r.building_id
                    JOIN assessments AS a
                       ON r.assessment_id = a.id
                    JOIN questions AS q
                       ON r.question_id = q.id
                    WHERE yn IS FALSE AND assessment_id = %s AND county = %s;""",
                (assessment_id, county,)
    )
    query = cur.fetchall()
    db.conn.commit()
    cur.close()

    # Get all the products caught by ner
    arr = []
    for [x] in query:
        dict = ner_sent(x)
        for i in dict["product_name"]:
            arr.append(i)

    # Count the top three
    times = []
    for ent in arr:
        temp = (ent, arr.count(ent),)
        if temp not in times:
            times.append(temp)
    times.sort(key=lambda tup: tup[1])

    # wrap
    ret = {}
    for c in range(len(times)):
        ret[c+1] = times[c]

    return ret
