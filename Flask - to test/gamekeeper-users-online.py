# select where id = usersOnline
# to be done in JS
def users_online():
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT COUNT(*) AS usersonline FROM Users''')
    result = cur.fetchall()
    s = "<div class=\"length\"><div class=\"title\">Users Online: </div><div class=\"totalNumber\"><b>"+str(result[0]['usersonline'])+"</b></div></div>"
    return s