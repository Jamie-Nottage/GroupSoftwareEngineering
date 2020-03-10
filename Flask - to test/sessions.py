def get_teamid(username):
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT teamId FROM Users WHERE username=%s ''' %username)
    result = cur.fetchall()
    teamid = result[0]['teamId']
    return teamid