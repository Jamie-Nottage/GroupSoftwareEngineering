# add game keeper 
def add_gamekeeper_db(name, surname, email, username, password):
    cur = mysql.connection.cursor()
    hashedPassword = sha256_crypt.hash(password)
    commit = ''' INSERT INTO Gamekeeper (fName, lName, emailAddress, username, password) VALUES (?,?,?,?,?)'''
    cur.execute(commit,name,surname,email,username,hashedPassword)
    mysql.connection.commit()
    return 0