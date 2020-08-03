import ast
from chat_module.ner.demo import ner_sent

def overall(payload, db):
    payload = ast.literal_eval(payload)
    assessment_id = payload["assessment_id"]

    data = {}
    cur = db.conn.cursor()

    # 1. get counties
    cur.execute('SELECT * FROM counties')
    ret = cur.fetchall()

    for _, county in ret:
        data[county] = {
            # "check_ratio": 1,
            "checked_num": 0,
            "uncheck_num": 0,
            "TBD": { "Quick": 0, "Normal": 0, "Indoors": 0, "Corridor": 0, "Outdoors": 0, },
            "ner": {},
        }

        # 2. get schools
        cur.execute("""SELECT s.id AS id, s.name AS school_name
                       FROM schools AS s
                       JOIN contacts AS c
                          ON s.id = c.school_id
                       WHERE s.county = %s;""", (county,))
        schools = cur.fetchall()

        for school_id, _ in schools:
            # 3. get buildings
            cur.execute("""WITH answered AS (
                               SELECT r.building_id, COUNT(r.yn) AS COUNT
                               FROM responses AS r
                               JOIN buildings AS b
                                  ON r.building_id = b.id
                               WHERE assessment_id = %s AND b.school_id = %s
                               GROUP BY r.building_id
                            )

                            SELECT b.id AS building_id, b.name AS building_name,
                                   CASE WHEN a.count IS NOT NULL THEN TRUE
                                     ELSE FALSE END AS yn
                            FROM buildings AS b
                            JOIN schools AS s
                               ON b.school_id = s.id
                            FULL JOIN answered AS a
                               ON b.id = a.building_id
                            WHERE s.id = %s;"""
                            % (assessment_id, school_id, school_id),
            )
            buildings = cur.fetchall()
            for building_id, _, checked in buildings:
                if not checked:
                    data[county]["uncheck_num"] += 1
                else:
                    data[county]["checked_num"] += 1
                    cur.execute(
                        """SELECT q.id AS abs_q
                           FROM questions AS q
                           JOIN responses AS r
                              ON r.question_id = q.id
                           JOIN buildings AS b
                              ON b.id = r.building_id
                           WHERE (yn IS FALSE AND building_id = %s AND assessment_id = %s);""",
                        (building_id, assessment_id),
                    )
                    responses = cur.fetchall()
                    for q in responses:
                        if q[0] in range(1, 13): data[county]["TBD"]["Normal"] += 1
                        if q[0] in range(13, 33): data[county]["TBD"]["Indoors"] += 1
                        if q[0] in range(33, 46): data[county]["TBD"]["Corridor"] += 1
                        if q[0] in range(46, 65): data[county]["TBD"]["Outdoors"] += 1
                        if q[0] in range(65, 78): data[county]["TBD"]["Quick"] += 1
        if data[county]["checked_num"] + data[county]["uncheck_num"] > 0:
            data[county]["check_ratio"] = data[county]["checked_num"] / (data[county]["checked_num"] + data[county]["uncheck_num"])
        else:
            data[county]["check_ratio"] = 0

        # 4. ner result
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
        ner_ret = {}
        for c in range(len(times)):
            ner_ret[c+1] = times[c]

        data[county]["ner"] = ner_ret

    cur.close()
    db.conn.commit()
    return data
