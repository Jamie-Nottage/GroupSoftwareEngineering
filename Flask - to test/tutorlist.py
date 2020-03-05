# adding tutors into drop down list in signup page
# where id = tutors
def tutor_list():
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT title, fName, lName FROM Tutor''')
    result = cur.fetchall()
    s = ""
    for x in result:
        s += "<option class=\"options\" value="+str(x['fName'])+">"+str(x['title'])+" "+str(x['fName'])+" "+str(x['lName'])+"</option>"
    return s


