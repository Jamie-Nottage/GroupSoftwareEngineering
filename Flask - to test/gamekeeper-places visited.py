# select where id = placesVisited
# to be done in JS
def places_visited():
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT COUNT(*) AS placesvisited FROM VisitBuilding''')
    result = cur.fetchall()
    s = "<div class=\"length\"><div class=\"title\">Places Visited: </div><div class=\"totalNumber\"><b>"+ str(result[0]['placesvisited'])+"</b></div></div>"
    return s