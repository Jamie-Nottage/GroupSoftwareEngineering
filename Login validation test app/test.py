from flask import Flask, render_template, request, session, redirect, url_for
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
	if request.method == 'POST':
		if 'username' in session:
			return redirect(url_for('index'))
		else:
			if validateLogin(request.form["username"], request.form["password"]) == 0:
				return redirect(url_for('main_app'))
			else:
				return 'Not valid login'

@app.route('/login-page')
def login_page():
	return render_template('login-page.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		if verifySignup(request.form["firstname"], request.form["surname"], request.form["email"], request.form["username"], request.form["password"], request.form["tutor"]) == 0:
			return redirect(url_for('main_app'))
		else:
			return 'Signup failed'

@app.route('/signup-page')
def signup_page():
	return render_template('signup-page.html')

@app.route('/getTutors', methods=['POST','GET'])
def get_tutors():
	if request.method == 'POST':
		return tutor_list()
	return redirect(url_for('signup-page'))
	
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
	cur.execute('''SELECT * FROM Users WHERE username=\'%s\';''' % username)
	user = cur.fetchall()
	if not user:
		return 1
	else:
		hashedPassword = user[0]['password']
		if sha256_crypt.verify(password,hashedPassword):
			return 0
	return 1


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