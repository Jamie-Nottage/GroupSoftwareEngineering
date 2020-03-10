from flask import Flask, render_template, request, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = 'groupo@exeter-expedition-db'
app.config['MYSQL_PASSWORD'] = 'MatthewYates2000'
app.config['MYSQL_HOST'] = 'exeter-expedition-db.mysql.database.azure.com'
app.config['MYSQL_DB'] = 'GAME_DATABASE'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/game-keeper')
def game_keeper():
    return render_template('GameKeeper.html', users=users_online(), teams=game_leader_board(), places=places_visited())


@app.route('/add-game-keeper', methods=['POST', 'GET'])
def add_game_keeper():
    if request.method == 'POST':
        name = request.form["firstname"]
        surname = request.form["surname"]
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        add_game_keeper(name, surname, email, username, password)
    return render_template('AddGK.html')


@app.route('/add-tutor', methods=['POST', 'GET'])
def add_tutor():
    if request.method == 'POST':
        title = request.form["title"]
        name = request.form["firstname"]
        surname = request.form["surname"]
        add_tutor_db(title, name, surname)
    return render_template('addtutor.html')


@app.route('/get-leaderboard', methods=['POST', 'GET'])
def get_leaderboard_gk():
    if request.method == 'GET':
        teams = game_leader_board()
    return render_template('GameKeeper.html', teams=teams)

@app.route('/users-online', methods=['POST', 'GET'])
def get_users():
    if request.method == 'GET':
        users = users_online()
    return render_template('GameKeeper.html', users=users)

@app.route('/places-visited', methods=['POST', 'GET'])
def get_places():
    if request.method == 'GET':
        places = places_visited()
    return render_template('GameKeeper.html', places=places)


def add_gamekeeper_db(name, surname, email, username, password):
    cur = mysql.connection.cursor()
    hashedPassword = sha256_crypt.hash(password)
    cur.execute(
        ''' INSERT INTO Gamekeeper (fName, lName, emailAddress, username, password) VALUES (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')''' % (
        name, surname, email, username, hashedPassword))
    mysql.connection.commit()
    return 0


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


if __name__ == '__main__':
    app.run()
