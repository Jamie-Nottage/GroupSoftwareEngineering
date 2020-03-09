
def checkQR(QRcode, teamid):
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT COUNT(*) AS count FROM visited WHERE teamId=%d; ''' %int(teamid))
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
            # finding out if clues have been used for first stop
            cur.execute(''' SELECT count(*) AS count FROM usedclues WHERE buildingId=(SELECT buildingId FROM Building WHERE verificationCode=\'%s\') AND teamId=%d; ''' %(QRcode, int(teamid)))
            count = cur.fetchall
            if count[0]['count'] == 1:
                cur.execute('''UPDATE Score SET clueLevel=2 WHERE taskId=(SELECT taskId FROM Task WHERE buildingId=(SELECT buildingId FROM Building WHERE verificationCode=\'%s\') and required=1) AND teamId=%d;''' %(QRcode,int(teamid)))
                mysql.connection.commit()   
            elif count[0]['count'] == 2:
                cur.execute('''UPDATE Score SET clueLevel=3 WHERE taskId=(SELECT taskId FROM Task WHERE buildingId=(SELECT buildingId FROM Building WHERE verificationCode=\'%s\') and required=1) AND teamId=%d;''' %(QRcode,int(teamid)))
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
        # finding out if clues have been used for rest
        cur.execute(''' SELECT count(*) AS count FROM usedclues WHERE buildingId=(SELECT buildingId FROM Building WHERE verificationCode=\'%s\') AND teamId=%d; ''' %(QRcode, int(teamid)))
        count = cur.fetchall
            if count[0]['count'] == 1:
                cur.execute('''UPDATE Score SET clueLevel=2 WHERE taskId=(SELECT taskId FROM Task WHERE buildingId=(SELECT buildingId FROM Building WHERE verificationCode=\'%s\') and required=1) AND teamId=%d;''' %(QRcode,int(teamid)))
                mysql.connection.commit()   
            elif count[0]['count'] == 2:
                cur.execute('''UPDATE Score SET clueLevel=3 WHERE taskId=(SELECT taskId FROM Task WHERE buildingId=(SELECT buildingId FROM Building WHERE verificationCode=\'%s\') and required=1) AND teamId=%d;''' %(QRcode,int(teamid)))
                mysql.connection.commit()
        return "true"