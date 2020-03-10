def display_achievements(teamid):
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT COUNT(*) AS count FROM visited WHERE teamId=%d; ''' %int(teamid))
    result = cur.fetchall()
    s = "<h2>Extra Achievements</h2><table><tr><th>Task Description</th><th>Points</th></tr>"
    if result[0]['count'] == 0:
        cur.execute(''' SELECT * FROM Task WHERE required=0 AND buildingId=6; ''')
        task1 = cur.fetchall()
        s += "<tr><td>"+ str(task1[0]['description']) +"</td><td>"+ str(task1[0]['points']) +"</td></tr></table>"
        return s
    else:
        cur.execute(''' SELECT * FROM Task WHERE required=0 AND buildingId=(SELECT buildingId FROM Route WHERE stopNo=(SELECT stopNo FROM Route WHERE pathId=%d and buildingId=(SELECT buildingId FROM visited WHERE teamId=%d LIMIT 1) + 1);''' % (int(teamid), int(teamid)))
        tasks = cur.fetchall()
        for x in tasks:
            s += "<tr><td>"+ str(x['description']) +"</td><td>"+ str(x['points']) +"</td></tr>"
        s += "</table>"
        return s