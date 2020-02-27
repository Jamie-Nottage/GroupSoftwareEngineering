from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = 'groupo@exeter-expedition-db'
app.config['MYSQL_PASSWORD'] = 'MatthewYates2000'
app.config['MYSQL_HOST'] = 'exeter-expedition-db.mysql.database.azure.com'
app.config['MYSQL_DB'] = 'GAME_DATABASE'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    return main_app()

@app.route('/main')
def main_app():
    return render_template('index.html')

@app.route('/getSign', methods=['POST','GET'])
def get_sign():
    if request.method == 'POST':
        team_name = request.form["teamname"]
        return getNextLocation(team_name)
    return main_app()

@app.route('/checkIn', methods=['POST', 'GET'])
def check_in():
    if request.method == 'POST':
        team_name = request.form["teamname"]
        qr_string = request.form["qrstring"]
        return checkQR(qr_string, team_name)
    return main_app

@app.route('/qrdemo')
def qrdemo():
    return render_template('qrdemo.html')

@app.route('/getCentralTable', methods=['POST', 'GET'])
def get_central_table():
    if request.method == 'POST':
        team_name = request.form["teamname"]
        return taskDisplay(team_name)
    return main_app

'''def getNextLocation(team):
    cur = mysql.connection.cursor()
    cur.execute(''''''SELECT buildingName FROM Building
	WHERE buildingId = (SELECT buildingId FROM Route
		WHERE stopNo=
			(SELECT stopNo FROM Route
			WHERE pathId=(SELECT teamId FROM visited WHERE teamId=%d LIMIT 1)
			AND buildingId=(SELECT buildingId FROM visited WHERE teamId=%d LIMIT 1))+1
		AND pathId=(SELECT teamId FROM visited WHERE teamId=%d LIMIT 1));'''''' % (int(team), int(team), int(team)))
    result = cur.fetchall();
    return result[0]["buildingName"]'''

def getNextLocation(teamid):
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT COUNT(*) AS count FROM visited; ''')
    first = cur.fetchall();
    if first[0]['count'] == 0:
        cur.execute(''' SELECT buildingName FROM Building WHERE buildingId = (SELECT buildingId FROM Route WHERE stopNo=1 AND pathId=%d); ''' %int(teamid))
        firststop = cur.fetchall();
        return firststop[0]['buildingName']
    else:
        cur.execute('''SELECT buildingName FROM Building WHERE buildingId = (SELECT buildingId FROM Route WHERE stopNo=(SELECT stopNo FROM Route WHERE pathId=(SELECT teamId FROM visited WHERE teamId=%d LIMIT 1) AND buildingId=(SELECT buildingId FROM visited WHERE teamId=%d LIMIT 1))+1 AND pathId=(SELECT teamId FROM visited WHERE teamId=%d LIMIT 1));''' % (int(teamid), int(teamid), int(teamid)))
        result = cur.fetchall();
    cur.execute(''' SELECT buildingId FROM Route WHERE pathId=%d AND stopNo=(SELECT count(*) FROM Route WHERE pathId=%d); ''' % (int(teamid), int(teamid)))
    finalstop = cur.fetchall();
    cur.execute(''' SELECT buildingId FROM visited LIMIT 1; ''')
    current = cur.fetchall();
    if finalstop[0]['buildingId'] == current[0]['buildingId']:
        return "Game Completed"
    return result[0]['buildingName']

def checkQR(QRcode, teamid):
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT COUNT(*) AS count FROM visited; ''')
    first = cur.fetchall();
    if first[0]['count'] == 0:
        cur.execute(''' SELECT verificationCode FROM Building WHERE buildingId = (SELECT buildingId FROM Route WHERE stopNo=1 AND pathId=%d); ''' %int(teamid))
        firststop = cur.fetchall();
        if firststop[0]["verificationCode"] != QRcode:
            return "false"
        else:
            cur.execute('''INSERT INTO VisitBuilding VALUES ((SELECT buildingId FROM Building WHERE verificationCode=\'%s\'), %d, NOW());''' %(QRcode, int(teamid)))
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
        return "true"

def taskDisplay(teamId):
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT * FROM visited WHERE teamId=%d; ''' % int(teamId))
    result = cur.fetchall();
    s = ""
    for x in result:

        s = s + "<li><div class=\"cl-element prev\"><div class=\"cl-element left prev\"><img src=\"static/img/"+ x['imageSource'] +"\" alt=\" "+ x['buildingName'] + "\" height=\"65\" class=\"grey-img\"><img src=\"static/img/tick.png\" alt=\"Tick\" height=\"60\" class=\"tick-img\"></div><p class=\"visited title\">"+ x['buildingName'] +"</p><p class=\"visited date\">" + str(x['time']).split(" ")[0] + "</p><p class=\"visited points\">Time Visited: " + str(x['time']).split(" ")[1] + "</p></div></li>"
    return s

#leaderboard
def leaderboard():
    cur.mysql.connection.cursor()
    cur.execute('''SELECT * FROM leaderboard''')
    result = cur.fetchall()
    s = "<table><tr><th>Team</th><th>Score</th></tr>"
    for x in result:
        s += "<tr><td>" + str(x['teamName']) + "</td><td>"+ str(x['score']) +"</td>"
    s += "</table>"
    return s

#endscreen

if __name__ == '__main__':
    app.run(host='0.0.0.0')
