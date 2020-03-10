from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt

app = Flask(__name__)

app.config['MYSQL_USER'] = 'groupo@exeter-expedition-db'
app.config['MYSQL_PASSWORD'] = 'MatthewYates2000'
app.config['MYSQL_HOST'] = 'exeter-expedition-db.mysql.database.azure.com'
app.config['MYSQL_DB'] = 'GAME_DATABASE'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
	if 'username' in session:
		return 'Logged in as ' + session['username']
	return redirect(url_for('home_page'))
	
@app.route('/main')
def main_app():
	return render_template('index.html')
	
@app.route('/home')
def home_page():
	return render_template('home-page.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if 'username' in session:
			return redirect(url_for('index'))
		else:
			valid = validateLogin(request.form["username"], request.form["password"])
			if valid == 0:
				return redirect(url_for('main_app'))
			elif valid == 1:
				return redirect(url_for('game_keeper'))
			else:
				error = True
	return render_template('login-page.html', loginError=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	error = None
	if request.method == 'POST':
		if verifySignup(request.form["firstname"], request.form["surname"], request.form["email"], request.form["username"], request.form["password"], request.form["tutor"]) == 0:
			return redirect(url_for('main_app'))
		else:
			error = True
	return render_template('signup-page.html', signupError=error)

@app.route('/getTutors', methods=['POST','GET'])
def get_tutors():
	if request.method == 'POST':
		return tutor_list()
	return redirect(url_for('signup'))
	
@app.route('/terms')
def terms_page():
	return render_template('terms-page.html')

@app.route('/privacy')
def privacy_page():
	return render_template('privacy-page.html')
	
# adding tutors into drop down list in signup page
def tutor_list():
	cur = mysql.connection.cursor()
	cur.execute(''' SELECT title, fName, lName FROM Tutor''')
	result = cur.fetchall()
	s = "<option class=\"options\" value=\"\" disabled selected hidden>Please select a tutor</option>"
	for x in result:
		s += "<option class=\"options\" value=\""+str(x['fName'])+" "+str(x['lName'])+"\">"+str(x['title'])+" "+str(x['fName'])+" "+str(x['lName'])+"</option>"
	return s

def validateLogin(username, password):
	cur = mysql.connection.cursor()
	cur.execute('''SELECT username, password FROM Users WHERE username=\'%s\' LIMIT 1;''' % username)
	user = cur.fetchall()
	cur.execute('''SELECT username, password FROM Gamekeeper WHERE username=\'%s\' LIMIT 1;''' % username)
	tutor = cur.fetchall()
	if user:
		hashedPassword = user[0]['password']
		if sha256_crypt.verify(password,hashedPassword):
			return 0
	elif tutor:
		hashedPassword = tutor[0]['password']
		if sha256_crypt.verify(password,hashedPassword):
			return 1
	return -1

def verifySignup(name, surname, email, username, password, tutor):
	cur = mysql.connection.cursor()
	cur.execute('''SELECT * FROM Users WHERE username=\'%s\' OR emailAddress=\'%s\';''' % (username, email))
	user = cur.fetchall()
	if user:
		return 1
	else:
		x = tutor.split(' ')
		tutorFName = x[0]
		tutorLName = x[1]
		cur.execute('''SELECT tutorId FROM Tutor WHERE fName=\'%s\' OR lName=\'%s\' LIMIT 1;''' % (tutorFName,tutorLName))
		tutor = cur.fetchall()
		tutorID = tutor[0]['tutorId']
		hashedPassword = sha256_crypt.hash(password)
		cur.execute('''INSERT INTO Users (fName, lName, emailAddress, username, password, tutorId, teamId) VALUES (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',%d,%d)''' % (name, surname, email, username, hashedPassword, tutorID, tutorID))
		mysql.connection.commit()
		return 0
		
#BEN RAF CODE#
@app.route('/game-keeper')
def game_keeper():
    return render_template('game-keeper-page.html', users=users_online(), teams=game_leader_board(), places=places_visited())

@app.route('/add-tutor', methods=['POST', 'GET'])
def add_tutor():
    if request.method == 'POST':
        title = request.form["title"]
        name = request.form["firstname"]
        surname = request.form["surname"]
        add_tutor_db(title, name, surname)
    return render_template('add-tutor.html')

@app.route('/add-game-keeper', methods=['POST', 'GET'])
def add_game_keeper():
    if request.method == 'POST':
        name = request.form["firstname"]
        surname = request.form["surname"]
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        add_game_keeper_db(name, surname, email, username, password)
    return render_template('add-game-keeper.html')

@app.route('/get-leaderboard', methods=['POST', 'GET'])
def get_leaderboard_gk():
    if request.method == 'GET':
        teams = game_leader_board()
    return render_template('add-game-keeper.html', teams=teams)

@app.route('/users-online', methods=['POST', 'GET'])
def get_users():
    if request.method == 'GET':
        users = users_online()
    return render_template('add-game-keeper.html', users=users)

@app.route('/places-visited', methods=['POST', 'GET'])
def get_places():
    if request.method == 'GET':
        places = places_visited()
    return render_template('add-game-keeper.html', places=places)

def add_tutor_db(title, firstname, lastname):
    cur = mysql.connection.cursor()
    cur.execute(''' INSERT INTO Tutor VALUES (NULL, \'%s\', \'%s\', \'%s\')''' % (title, firstname, lastname))
    mysql.connection.commit()
    cur.execute(''' SELECT COUNT(*) AS count from Tutor; ''')
    tutor_count = cur.fetchall()
    cur.execute(''' SELECT COUNT(*) AS count from Paths; ''')
    path_count = cur.fetchall()
    if path_count[0]['count'] < tutor_count[0]['count']:
        cur.execute(''' INSERT INTO Paths VALUES (NULL, 6)''')
        mysql.connection.commit()
    cur.execute(
        '''SELECT COUNT(*) AS count FROM Route WHERE pathId=(SELECT tutorId FROM Tutor WHERE title=\'%s\' AND fName=\'%s\' AND lName=\'%s\')''' % (
        title, firstname, lastname))
    route_count = cur.fetchall()
    if route_count[0]['count'] == 0:
        # must enter a new route before can enter a new tutor.
        # response must be done
        return 1
    teamname = "Team " + firstname + " " + lastname
    cur.execute(
        ''' INSERT INTO Team VALUES (NULL, \'%s\', (SELECT tutorId FROM Tutor WHERE title=\'%s\' AND fName=\'%s\' AND lName=\'%s\'), (SELECT tutorId FROM Tutor WHERE title=\'%s\' AND fName=\'%s\' AND lName=\'%s\') )''' % (
        teamname, title, firstname, lastname, title, firstname, lastname))
    mysql.connection.commit()
    return 0

def add_game_keeper_db(name, surname, email, username, password):
    cur = mysql.connection.cursor()
    hashedPassword = sha256_crypt.hash(password)
    cur.execute(
        ''' INSERT INTO Gamekeeper (fName, lName, emailAddress, username, password) VALUES (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')''' % (
        name, surname, email, username, hashedPassword))
    mysql.connection.commit()
    return 0

def game_leader_board():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM leaderboard''')
    result = cur.fetchall()
    return result

def places_visited():
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT COUNT(*) AS placesvisited FROM VisitBuilding''')
    result = cur.fetchall()
    return result

def users_online():
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT COUNT(*) AS usersonline FROM Users''')
    result = cur.fetchall()
    return result

#BEN RANG CODE#		
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

def getNextLocation(teamid):
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT COUNT(*) AS count FROM visited WHERE teamId=%d ''' %int(teamid))
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
    cur.execute(''' SELECT COUNT(*) AS count FROM visited WHERE teamId=%d; ''' %int(teamid))
    first = cur.fetchall();
    if first[0]['count'] == 0:
        cur.execute(''' SELECT verificationCode FROM Building WHERE buildingId = (SELECT buildingId FROM Route WHERE stopNo=1 AND pathId=%d); ''' %int(teamid))
        firststop = cur.fetchall();
        if firststop[0]["verificationCode"] != QRcode:
            return "false"
        else:
            cur.execute('''INSERT INTO VisitBuilding VALUES ((SELECT buildingId FROM Building WHERE verificationCode=\'%s\'), %d, NOW());''' %(QRcode, int(teamid)))
            mysql.connection.commit()
            cur.execute('''INSERT INTO Score VALUES (NULL, DEFAULT, (SELECT taskId from Task where buildingId=(SELECT buildingId FROM Building WHERE verificationCode=\'%s\') and required=1), %d);''' %(QRcode, int(teamid)))
            mysql.connection.commit()
            # finding out if clues have been used for first stop
            cur.execute(''' SELECT count(*) AS count FROM usedclues WHERE buildingId=(SELECT buildingId FROM Building WHERE verificationCode=\'%s\') AND teamId=%d; ''' %(QRcode, int(teamid)))
            count = cur.fetchall()
            if count[0]['count'] == 1:
                cur.execute('''UPDATE Score SET clueLevel=2 WHERE taskId=(SELECT taskId FROM Task WHERE buildingId=(SELECT buildingId FROM Building WHERE verificationCode=\'%s\') and required=1) AND teamId=%d;''' %(QRcode,int(teamid)))
                mysql.connection.commit()
            elif count[0]['count'] == 2:
                cur.execute('''UPDATE Score SET clueLevel=3 WHERE taskId=(SELECT taskId FROM Task WHERE buildingId=(SELECT buildingId FROM Building WHERE verificationCode=\'%s\') and required=1) AND teamId=%d;''' %(QRcode,int(teamid)))
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
        cur.execute('''INSERT INTO Score VALUES (NULL, DEFAULT, (SELECT taskId from Task where buildingId=(SELECT buildingId FROM Building WHERE verificationCode=\'%s\') and required=1), %d);''' %(QRcode, int(teamid)))
        mysql.connection.commit()
        # finding out if clues have been used for rest
        cur.execute(''' SELECT count(*) AS count FROM usedclues WHERE buildingId=(SELECT buildingId FROM Building WHERE verificationCode=\'%s\') AND teamId=%d; ''' %(QRcode, int(teamid)))
        count = cur.fetchall()
        if count[0]["count"] == 1:
            cur.execute('''UPDATE Score SET clueLevel=2 WHERE taskId=(SELECT taskId FROM Task WHERE buildingId=(SELECT buildingId FROM Building WHERE verificationCode=\'%s\') and required=1) AND teamId=%d;''' %(QRcode,int(teamid)))
            mysql.connection.commit()
        elif count[0]['count'] == 2:
            cur.execute('''UPDATE Score SET clueLevel=3 WHERE taskId=(SELECT taskId FROM Task WHERE buildingId=(SELECT buildingId FROM Building WHERE verificationCode=\'%s\') and required=1) AND teamId=%d;''' %(QRcode,int(teamid)))
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

@app.route('/getLeaderboard', methods=['POST', 'GET'])
def get_leaderboard():
    if request.method == 'GET':
        return str(leaderboard())
    return main_app

#leaderboard
def leaderboard():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM leaderboard''')
    result = cur.fetchall()
    s = "<table id=\"leaderboard-table\"><thead><tr class=\"leaderboard-row\"><th class=\"leaderboard-header\">Team</th><th class=\"leaderboard-header\">Score</th></tr></thead>"
    s += "<tbody>"
    for x in result:
        s += "<tr class=\"leaderboard-row\"><td class=\"leaderboard-data\">" + str(x['teamName']) + "</td><td class=\"leaderboard-data\">"+ str(x['score']) +"</td></tr>"
    s += "</tbody></table>"
    return s


def display_hint_level(teamid):
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
        cur.execute(''' SELECT COUNT(*) AS count FROM Used WHERE teamId=%d and clueId=%d ''' %(int(teamid),int(clueid[0]['clueId'])))
        is_used = cur.fetchall()
        if is_used[0]['count'] == 0:
            cur.execute(''' SELECT DISTINCT description FROM Clue WHERE clueLevel=%d ''' %clue_level)
            description = cur.fetchall()
            hint = clue_level - 1
            return hint
    return 3

@app.route('/displayClueContent', methods=['POST', 'GET'])
def display_clue_content():
    if request.method == 'GET':
        #team_name = request.form["teamname"]
        clue_tuple = clue_content(1)
        return jsonify(clue_list_content=clue_tuple[0], clue_img=clue_tuple[1], clue_level=clue_tuple[2])
    return main_app()

'''
    Returns a two-tuple. [0] contains the HTML content to go inside the clue
    container, [1] contains the img tag to be placed inside the overlay
    container for the image clue.
'''
def clue_content(team_name):
    clue_container_content = ""
    hint_level = display_hint_level(team_name)
    image_tag_content = ""

    #clue 1 content (either slider to clue itself)
    if (hint_level == 1):
        clue_container_content += '<li><div id="clue1-container" class="cl-element hint"><p id="clue1-txt" class="hint-main-txt">Slide to reveal a clue (-25 points)</p><div id="clue1" class="cl-element left"><img id="clue1-img" src="static/img/rightarrow.png" alt="->" height="50"class="clue-button-art"></div></div></li>'
    else:
        clue_txt = get_clue(team_name, 2);
        clue_container_content += '<li><div id="uncovered-clue1-container" class="cl-element hint"><p id="uncovered-clue1-txt" class="hint-main-txt uncovered">' + clue_txt + '</p>  </div>  </li>'

    #clue 2 content (either empty or slider or button to open container)
    if (hint_level == 1):
        clue_container_content += ""
    elif (hint_level == 2):
        clue_container_content += '<li><div id="clue2-container" class="cl-element hint"><p id="clue2-txt" class="hint-main-txt">Slide to reveal a photo (-50 points)</p><div id="clue2" class="cl-element left"><img id="clue2-img" src="static/img/rightarrow.png" alt="->" height="50"class="clue-button-art"></div></div></li>'
    else:
        clue_txt = get_clue(team_name, 3);
        image_tag_content = "static/img/" + clue_txt;
        clue_container_content += '<li><div id="uncovered-clue2-container" class="cl-element hint"><div id="uncovered-clue2-button" onclick="setTimeout(revealPhoto, 2)">Reveal photo</div>  </div>  </li>'


    return (clue_container_content, image_tag_content, hint_level)


@app.route('/unlockClue', methods=['POST', 'GET'])
def get_unlock_clue():
    if request.method == 'GET':
        return str(unlock_clue(1))
    return main_app()

def unlock_clue(teamid):
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
        s += result[0]['clue']
        cur.execute(''' SELECT clueId FROM BuildingClue WHERE buildingId=%d and clueLevel=%d ''' %(buildingid,clue_level))
        clueid = cur.fetchall()
        cur.execute(''' INSERT INTO Used VALUES (%d, %d)''' % (int(clueid[0]['clueId']),int(teamid)))
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
        cur.execute(''' INSERT INTO Used VALUES (%d, %d)''' %(int(clueid[0]['clueId']),int(teamid)))
        mysql.connection.commit()
        return s

def get_clue(teamid, clue_level):
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
    if clue_level == 2:
        cur.execute(''' SELECT clue FROM BuildingClue WHERE buildingId=%d and clueLevel=%d ''' %(buildingid,clue_level))
        result = cur.fetchall()
        s += result[0]['clue']
        cur.execute(''' SELECT clueId FROM BuildingClue WHERE buildingId=%d and clueLevel=%d ''' %(buildingid,clue_level))
        clueid = cur.fetchall()
        return s
    if clue_level == 3:
        cur.execute(''' SELECT clue FROM BuildingClue WHERE buildingId=%d and clueLevel=%d ''' %(buildingid,clue_level))
        result = cur.fetchall()
        cur.execute(''' SELECT buildingName FROM Building WHERE buildingId=%d ''' %buildingid)
        building = cur.fetchall()
        s += result[0]['clue'];
        cur.execute(''' SELECT clueId FROM BuildingClue WHERE buildingId=%d and clueLevel=%d ''' %(buildingid,clue_level))
        clueid = cur.fetchall()
        return s

@app.route('/displayAchievements', methods=['GET'])
def display_achievements_content():
    if request.method == 'GET':
        return display_achievements(1)
    return main_app()

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
        cur.execute(''' SELECT * FROM Task WHERE required=0 AND buildingId=(SELECT buildingId FROM visited WHERE teamId=%d LIMIT 1); '''%int(teamid))
        tasks = cur.fetchall()
        for x in tasks:
            s += "<tr><td>"+ str(x['description']) +"</td><td>"+ str(x['points']) +"</td></tr>"
        s += "</table>"
        return s