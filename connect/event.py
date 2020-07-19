def event(db):
    cur = db.conn.cursor()
    cur.execute('SELECT * FROM assessments')
    result = cur.fetchall()

    data = {}
    for ass_id, event, time in result:
        data[ass_id] = {"assessment_id": ass_id, "event": event, "time": time}

    db.conn.commit()
    cur.close()
    return data
