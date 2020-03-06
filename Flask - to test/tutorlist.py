# adding tutors into drop down list in signup page
# where id = tutors
def tutor_list():
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT title, fName, lName FROM Tutor''')
    result = cur.fetchall()
    s = "<option class=\"options\" value=\"\" disabled selected hidden>Please select a tutor</option>"
    for x in result:
        s += "<option class=\"options\" value="+str(x['fName'])+">"+str(x['title'])+" "+str(x['fName'])+" "+str(x['lName'])+"</option>"
    return s


