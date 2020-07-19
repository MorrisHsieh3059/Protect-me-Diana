import ast

def fetch(payload, db):
    payload = ast.literal_eval(payload)
    county = payload["county"]
    assessment_id = payload["assessment_id"]

    cur = db.conn.cursor()
    cur.execute("""SELECT s.id AS id, s.name AS school_name,
                          s.county AS county, s.address AS address,
                          s.latitude AS latitude, s.longitude AS longitude,
                          c.name AS name, c.phone AS phone, c.id AS userid
                   FROM schools AS s
                   JOIN contacts AS c
                      ON s.id = c.school_id
                   WHERE s.county = %s;""", (county,))
    schools = cur.fetchall()

    data = {}
    for i in range(len(schools)):
        data[schools[i][1]] = {
            "school_name": schools[i][1],
            "school_id": schools[i][0],
            "county": schools[i][2],
            "address": schools[i][3],
            "latitude": str(schools[i][4]),
            "longitude": str(schools[i][5]),
            "name": schools[i][6],
            "phone": schools[i][7],
            "userid": schools[i][8],
        }

        # calculate how many buildings have examined
        cur.execute("""WITH answered AS (
                           SELECT r.building_id, COUNT(r.yn) AS COUNT
                           FROM responses AS r
                           JOIN buildings AS b
                              ON r.building_id = b.id
                           WHERE assessment_id = %s AND b.school_id = %s
                           GROUP BY r.building_id
                        )

                        SELECT CASE WHEN a.count IS NOT NULL THEN TRUE
                                 ELSE FALSE END AS yn
                        FROM buildings AS b
                        JOIN schools AS s
                           ON b.school_id = s.id
                        FULL JOIN answered AS a
                           ON b.id = a.building_id
                        WHERE s.id = %s;"""
                    % (assessment_id, schools[i][0], schools[i][0]),
        )

        ret = cur.fetchall()
        total_building = len(ret)
        checked_building = 0
        for status in ret:
            if status[0]: checked_building += 1

        data[schools[i][1]]["YN"] = f"{checked_building}/{total_building}"
        data[schools[i][1]]["severity"] = round(checked_building/total_building*100)


    db.conn.commit()

    cur.close()
    return data
