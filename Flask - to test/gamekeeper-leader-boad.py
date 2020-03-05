# select where id = container
# to be done in JS
def game_leader_board():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM leaderboard''')
    result = cur.fetchall()
    s = ""
    for x in result:
        s += "<div class=\"row\"><div class=\"name\">"+str(x['teamName'])+"</div><div class=\"score\">"+str(x['score'])+"</div></div>"
    return s