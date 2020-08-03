import ast

def building(payload, db):
    payload = ast.literal_eval(payload)
    school_id = payload["school_id"]
    assessment_id = payload["assessment_id"]

    cur = db.conn.cursor()
    cur.execute("""WITH answered AS (
                       SELECT r.building_id, COUNT(r.yn) AS COUNT
                       FROM responses AS r
                       JOIN buildings AS b
                          ON r.building_id = b.id
                       WHERE assessment_id = %s AND b.school_id = %s
                       GROUP BY r.building_id
                    )

                    SELECT s.name AS school_name, b.id AS building_id, b.name AS building_name,
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

    ret = cur.fetchall()
    db.conn.commit()

    data = {}
    data["assessment_id"] = assessment_id
    data["building_id"] = []
    data["building_name"] = []
    data["yn"] = []
    data["severity"] = []
    data["school_name"] = ret[0][0] if len(ret) > 0 else ""

    for _, building_id, building_name, yn in ret:
        data["building_id"].append(building_id)
        data["building_name"].append(building_name)
        data["yn"].append(yn)

    for i in range(len(data["building_id"])):
        if not data["yn"][i]:                # 沒填過
            data["severity"].append(0)
        else:
            building_id = data["building_id"][i]
            cur.execute("""SELECT * FROM responses WHERE (building_id = '%s' AND assessment_id = %s)""" % (building_id, assessment_id),)
            sheet = cur.fetchall()
            fenshu = 0
            y_n = []

            for j in range(len(sheet)):
                y_n.append(sheet[j][0])

            if 0 not in y_n:
               fenshu = 100
            elif 0 in y_n[0:64]:
                for k in range(64):
                    if y_n[k] == 1:
                        fenshu += 100/64
            elif 0 in y_n[64:77]:
                for k in range(64,77):
                    if y_n[k] == 1:
                        fenshu += 100/13

            fenshu = round(fenshu)
            data["severity"].append(fenshu)
            db.conn.commit()

    return data
