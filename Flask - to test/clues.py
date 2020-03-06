def display_hint_html(teamid):
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT COUNT(*) AS count FROM visited WHERE teamId=%d; ''' %int(teamid))
    first = cur.fetchall()
    if first[0]['count'] == 0:
        buildingid = 6
    else:
        cur.execute('''SELECT buildingId FROM Route WHERE stopNo= (SELECT stopNo FROM Route WHERE pathId=(SELECT teamId FROM visited WHERE teamId=%d LIMIT 1)AND buildingId=(SELECT buildingId FROM visited WHERE teamId=%d LIMIT 1))+1 AND pathId=(SELECT teamId FROM visited WHERE teamId=%d LIMIT 1);''' % (int(teamid), int(teamid), int(teamid)))
        result = cur.fetchall()
        buildingid = result[0]['buildingId']
    s = ""
    cur.execute(''' SELECT DISTINCT clueLevel FROM BuildingClue; ''')
    no_of_clues = cur.fetchall()
    for x in no_of_clues:
        clue_level = x['clueLevel']
        cur.execute(''' SELECT clueId FROM BuildingClue WHERE buildingId=%d and clueLevel=%d ''' %(buildingid,clue_level))
        clueid = cur.fetchall()
        cur.execute(''' SELECT COUNT(*) AS count FROM Used WHERE teamId=%d and clueId=%d ''' %(int(teamid),clueid))
        is_used = cur.fetchall()
        if is_used[0]['count'] == 0:
            cur.execute(''' SELECT DISTINCT description FROM Clue WHERE clueLevel=%d ''' %clue_level)
            description = cur.fetchall()
            hint = clue_level - 1
            s += "<li><div class=\"cl-element hint\"><div class=\"cl-element left\"><p class=\"hint-left-txt\">Hint "+hint+"</p></div><p class=\"hint-main-txt\">"+description[0]['description']+"</p></div></li>"
            return s


def display_clue(teamid):
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT COUNT(*) AS count FROM visited WHERE teamId=%d; ''' %int(teamid))
    first = cur.fetchall()
    if first[0]['count'] == 0:
        buildingid = 6
    else:
        cur.execute('''SELECT buildingId FROM Route WHERE stopNo= (SELECT stopNo FROM Route WHERE pathId=(SELECT teamId FROM visited WHERE teamId=%d LIMIT 1)AND buildingId=(SELECT buildingId FROM visited WHERE teamId=%d LIMIT 1))+1 AND pathId=(SELECT teamId FROM visited WHERE teamId=%d LIMIT 1);''' % (int(teamid), int(teamid), int(teamid)))
        result = cur.fetchall()
        buildingid = result[0]['buildingId']
    s = ""
    cur.execute(''' SELECT COUNT(*) AS count FROM usedclues WHERE teamId=%d AND buildingId=%d ''' %(int(teamid),buildingid))
    result = cur.fetchall()
    clue_level = result[0]['count']+2
    if result[0]['count'] == 0:
        cur.execute(''' SELECT clue FROM BuildingClue WHERE buildingId=%d and clueLevel=%d ''' %(buildingid,clue_level))
        result = cur.fetchall()
        s += "<p>"+result[0]['clue']+"</p>"
        cur.execute(''' SELECT clueId FROM BuildingClue WHERE buildingId=%d and clueLevel=%d ''' %(buildingid,clue_level))
        clueid = cur.fetchall()
        cur.execute(''' INSERT INTO Used VALUES (%d, %d)''' %(clueid,int(teamid)))
        mysql.connection.commit()
        cur.execute(''' INSERT INTO Score VALUES (NULL, %d, (SELECT taskId FROM Task WHERE buildingId=%d and required=1),%d)''' %(clue_level,buildingId,int(teamid)))
        mysql.connection.commit()
        return s
    if result[0]['count'] == 1:
        cur.execute(''' SELECT clue FROM BuildingClue WHERE buildingId=%d and clueLevel=%d ''' %(buildingid,clue_level))
        result = cur.fetchall()
        cur.execute(''' SELECT buildingName FROM Building WHERE buildingId=%d ''' %buildingid)
        building = cur.fetchall()
        s += "<img src="+result[0]['clue']+" alt="+building[0]['buildingName']+">"
        cur.execute(''' SELECT clueId FROM BuildingClue WHERE buildingId=%d and clueLevel=%d ''' %(buildingid,clue_level))
        clueid = cur.fetchall()
        cur.execute(''' INSERT INTO Used VALUES (%d, %d)''' %(clueid,int(teamid)))
        mysql.connection.commit()
        cur.execute(''' INSERT INTO Score VALUES (NULL, %d, (SELECT taskId FROM Task WHERE buildingId=%d and required=1),%d)''' %(clue_level,buildingId,int(teamid)))
        mysql.connection.commit()
        return s


    
