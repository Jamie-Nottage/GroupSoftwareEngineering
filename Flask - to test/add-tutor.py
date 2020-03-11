# adding tutor to db adding team and making sure there is a path
def add_tutor_db(title, firstname, lastname):
    cur = mysql.connection.cursor()
    cur.execute(''' INSERT INTO Tutor VALUES (NULL, %s, %s, %s)''' %(title,firstname,lastname))
    mysql.connection.commit()
    cur.execute(''' SELECT COUNT(*) AS count from Tutor; ''')
    tutor_count = cur.fetchall()
    cur.execute(''' SELECT COUNT(*) AS count from Paths; ''')
    path_count = cur.fetchall()
    if path_count[0]['count'] < tutor_count[0]['count']:
        # must enter a new route before can enter a new tutor.
        # response must be done in JS
        return 1
    teamname = "Team " + firstname + " " + lastname
    cur.execute(''' INSERT INTO Team VALUES (NULL, %s, (SELECT tutorId FROM Tutor WHERE title=%s AND fName=%s AND lName=%s), (SELECT tutorId FROM Tutor WHERE title=%s AND fName=%s AND lName=%s) )''' %(teamname,title,firstname,lastname,title,firstname,lastname))
    mysql.connection.commit()
    return 0