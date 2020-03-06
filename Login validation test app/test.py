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

app.secret_key = b'BtE\x046X \xebs\x7f6\x98\x82\xe3\xc5\xca'

@app.route('/')
def index():
    if 'uname' in session:
        return 'Logged in as ' + session['uname']
    return redirect(url_for('home_page'))

@app.route('/home')
def home_page():
    return render_template('home-page.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'uname' in session:
            return redirect(url_for('index'))
        else:
            if validateLogin(request.form["username"], request.form["password"]) == 0:
                return redirect(url_for('index'))
            else:
                return 'Not valid login'
    else:
        return ''

@app.route('/login-page')
def login_page():
    return render_template('login-page.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if verifySignup(request.form["firstname"], request.form["surname"], request.form["email"], request.form["username"], request.form["password"], request.form["tutor"]) == 0:
            return redirect(url_for('index'))
        else:
            return 'Signup failed'
    else:
        return ''


@app.route('/signup-page')
def signup_page():
    return render_template('signup-page.html')


def validateLogin(username, password):
    cur = mysql.connection.cursor()
    query = '''SELECT * FROM Users WHERE username=?;'''
    cur.execute(query,username)
    user = cur.fetchall()
    if not user:
        return 1
    else:
        hashedPassword = user['password']
        if sha256_crypt.verify(password,hashedPassword):
            return 0
    return 1


def verifySignup(name, surname, email, username, password, tutor):
    cur = mysql.connection.cursor()
    query = '''SELECT * FROM Users WHERE username=? OR email=?;'''
    cur.execute(query,username,email)
    user = cur.fetchall()
    if not user:
        return 1
    else:
        x = tutor.split()
        tutorFName = x[0]
        tutorLName = x[1]
        tutors = '''SELECT * FROM Tutor WHERE fName=? OR lName=?;'''
        cur.execute(tutors,tutorFName,tutorLName)
        tutor = cur.fetchall()
        tutorID = tutor[tutorId]
        hashedPassword = sha256_crypt.hash(password)
        commit = '''INSERT INTO Users (fName, lName, emailAddress, username, password, tutorId, teamId)
                    VALUES (?,?,?,?,?,?,?)'''
        cur.execute(commit,name, surname, email, username, hashedPassword, tutorID, tutorID)
        mysql.connection.commit()
        return 0
