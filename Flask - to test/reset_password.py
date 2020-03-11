def reset_password(username, password, new_password):
    hashpwd = sha256_crypt.hash(password)
    new_hashpwd = sha256_crypt.hash(new_password)
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT COUNT(*) AS count FROM Gamekeeper WHERE username=\'%s\' AND password=\'%s\';''' %(username,hashpwd))
    count = cur.fetchall()
    if count[0]['count'] != 1:
        return 1
    else:
        cur. execute(''' UPDATE Gamekeeper SET password=\'%s\' WHERE password=\'%s\' ''' %(new_password, hashpwd))
        cur.connection.commit()
        return 0
