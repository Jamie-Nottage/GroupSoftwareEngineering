def individual_leaderboard_gk():
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT * FROM individualLeaderboard; ''')
    result = cur.fetchall()
    return s