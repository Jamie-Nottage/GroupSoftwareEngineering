def get_teamid(username):
    """
    Gets the teamid based on the username in the session
    :parameter username: The username is a session variable
    :return: Returns the teamid given the username
    :rtype: int.
    """
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT teamId FROM Users WHERE username=%s ''' %username)
    result = cur.fetchall()
    teamid = result[0]['teamId']
    return teamid

def get_userid(username):
    """
    Gets the userId based on the username in the session
    :parameter username: The username is a session variable
    :return: Returns the teamid given the username
    :rtype: int.
    """
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT userId FROM Users WHERE username=%s ''' %username)
    result = cur.fetchall()
    teamid = result[0]['userId']
    return teamid
