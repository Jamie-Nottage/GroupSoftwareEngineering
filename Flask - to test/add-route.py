def add_route_db(second, third, fourth, fifth, sixth):
    """
    Adding a new route to the database after the form has been submitted
    :param second: Name of the second building in the new route
    :param third: Name of the third building in the new route
    :param fourth: Name of the fourth building in the new route
    :param fifth: Name of the fifth building in the new route
    :param sixth: Name of the sixth building in the new route
    """
    cur = mysql.connection.cursor()
    cur.execute(''' INSERT INTO Paths VALUES (NULL, 6) ''')
    cur.connection.commit()
    buildingids = [6]
    cur.execute(''' SELECT pathId FROM Paths ORDER BY pathId DESC LIMIT 1 ''')
    pathid = cur.fetchall()
    cur.execute(''' SELECT buildingId FROM Building WHERE buildingName = %d ''' %second)
    sec = cur.fetchall()
    buildingids.append(sec[0]['buildingId'])
    cur.execute(''' SELECT buildingId FROM Building WHERE buildingName = %d ''' %third)
    thr = cur.fetchall()
    buildingids.append(thr[0]['buildingId'])
    cur.execute(''' SELECT buildingId FROM Building WHERE buildingName = %d ''' %fourth)
    four = cur.fetchall()
    buildingids.append(four[0]['buildingId'])
    cur.execute(''' SELECT buildingId FROM Building WHERE buildingName = %d ''' %fifth)
    fiv = cur.fetchall()
    buildingids.append(fiv[0]['buildingId'])
    cur.execute(''' SELECT buildingId FROM Building WHERE buildingName = %d ''' %sixth)
    six = cur.fetchall()
    buildingids.append(six[0]['buildingId'])
    for count in range(len(buildingids)):
        cur.execute(''' INSERT INTO Route VALUES (%d, %d, %d) ''' %(pathid[0]['pathId'], buildingids[count], count))
        cur.connection.commit()