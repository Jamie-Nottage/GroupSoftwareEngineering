def display_answers(taskid):
    cur = mysql.connection.cursor()
    s = "<table><tr><th>Select the Answer</th>"
    cur.execute(''' SELECT answer FROM achievementdetails WHERE taskId=%d; ''' %taskid)
    ans = cur.fetchall()
    for x in ans:
        s += "<tr><td>" + str(x['answer']) + "</td></tr>"
    s += "</table>"
    return s

def get_right_answer(taskid):
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT answer FROM achievementdetails WHERE taskId=%d and correct=1; ''' %taskid)
    ans = cur.fetchall()
    return ans

# test answer is correct before calling this function
def score(userid, taskid):
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT COUNT(*) AS count FROM UsersScore WHERE taskId=%d and userId=%d; ''' %(taskid,int(userid)))
    result = cur.fetchall()
    cur.execute(''' SELECT clueLevel FROM UsersScore WHERE taskId=%d and userId=%d; ''' %(taskid,int(userid)))
    clues = cur.fetchall()
    if result[0]['count'] == 0:
        cur.execute(''' INSERT INTO UsersScore VALUES (NULL, DEFAULT, %d, %d) ''' %(taskid,int(userid)))
        cur.connection.commit()
        
    elif result[0]['count'] == 1 and clues[0]['clueLevel'] == 1:
        cur.execute(''' UPDATE UsersScore SET clueLevel=5 WHERE taskId=%d and userId=%d; ''' %(taskid,int(userid)))
        cur.connection.commit()
        
    elif result[0]['count'] == 1 and clues[0]['clueLevel'] == 5:
        cur.execute(''' UPDATE AchievementUsed SET status=1, clueLevel=6 WHERE taskId=%d and userId=%d; ''' %(taskid,int(userid)))
        cur.connection.commit()
        
def individual_leaderboard():
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT * FROM individualLeaderboard; ''')
    result = cur.fetchall()
    s = "<table id=\"leaderboard-table\"><thead><tr class=\"leaderboard-row\"><th class=\"leaderboard-header\">Username</th><th class=\"leaderboard-header\">Score</th></tr></thead>"
    s += "<tbody>"
    for x in result:
        s += "<tr class=\"leaderboard-row\"><td class=\"leaderboard-data\">" + str(x['username']) + "</td><td class=\"leaderboard-data\">"+ str(x['score']) +"</td></tr>"
    s += "</tbody></table>"
    return s
    
    