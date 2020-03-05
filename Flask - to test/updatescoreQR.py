
def checkQR(QRcode, teamid):
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT COUNT(*) AS count FROM visited; ''')
    first = cur.fetchall();
    if first[0]['count'] == 0:
        cur.execute(''' SELECT verificationCode FROM Building WHERE buildingId = (SELECT buildingId FROM Route WHERE stopNo=1 AND pathId=%d); ''' %int(teamid))
        firststop = cur.fetchall();
        if firststop[0]["verificationCode"] != QRcode:
            return "false"
        else:
            cur.execute('''INSERT INTO VisitBuilding VALUES ((SELECT buildingId FROM Building WHERE verificationCode=\'%s\'), %d, NOW());''' %(QRcode, int(teamid)))
            mysql.connection.commit()
            cur.execute('''INSERT INTO Score VALUES (NULL, DEFAULT, (SELECT taskId from Task where buildingId=(SELECT buildingId FROM Building WHERE verificationCode=\'%s\') and required=1), %d);''' %(QRcode, int(teamid)))
            mysql.connection.commit()
            return "true"
    else:
        cur.execute('''SELECT verificationCode FROM Building WHERE buildingId = (SELECT buildingId FROM Route WHERE stopNo= (SELECT stopNo FROM Route WHERE pathId=(SELECT teamId FROM visited WHERE teamId=%d LIMIT 1)AND buildingId=(SELECT buildingId FROM visited WHERE teamId=%d LIMIT 1))+1 AND pathId=(SELECT teamId FROM visited WHERE teamId=%d LIMIT 1));''' % (int(teamid), int(teamid), int(teamid)))
        result = cur.fetchall();
    if result[0]["verificationCode"] != QRcode:
        return "false"
    else:
        cur.execute('''INSERT INTO VisitBuilding VALUES ((SELECT buildingId FROM Building WHERE verificationCode=\'%s\'), %d, NOW());''' %(QRcode, int(teamid)))
        mysql.connection.commit()
        cur.execute('''INSERT INTO Score VALUES (NULL, DEFAULT, (SELECT taskId from Task where buildingId=(SELECT buildingId FROM Building WHERE verificationCode=\'%s\') and required=1), %d);''' %(QRcode, int(teamid)))
        mysql.connection.commit()
        return "true"