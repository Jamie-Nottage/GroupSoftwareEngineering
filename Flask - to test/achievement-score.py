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
