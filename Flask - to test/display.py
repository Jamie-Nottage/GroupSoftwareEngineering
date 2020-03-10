def display_achievements(teamid):
    """
    Displays the achievments available for the current building
    :parameter teamid: A session variable, will be passed into the function based on who is logged into the system
    :return: Returns achievements in HTML string
    :rtype: String.
    """
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT COUNT(*) AS count FROM visited WHERE teamId=%d; ''' %int(teamid))
    result = cur.fetchall()
    s = ""
    if result[0]['count'] == 0:
        cur.execute(''' SELECT * FROM Task WHERE required=0 AND buildingId=6; ''')
        taskList = cur.fetchall()
        s += achievement_HTML(taskList)
    else:
        cur.execute('''SELECT * FROM Task WHERE required=0 AND buildingId = (SELECT buildingId FROM Route WHERE stopNo=(SELECT stopNo FROM Route WHERE pathId=(SELECT teamId FROM visited WHERE teamId=%d LIMIT 1) AND buildingId=(SELECT buildingId FROM visited WHERE teamId=%d LIMIT 1))+1 AND pathId=(SELECT teamId FROM visited WHERE teamId=%d LIMIT 1));''' % (int(teamid), int(teamid), int(teamid)))
        taskList = cur.fetchall()
        oldAchievements = cur.fetchall()
        s += achievement_HTML(taskList)
    s += '</ul>'
    return s

def achievement_HTML(taskList):
    """
    Renders the HTML template for each achievement and answers
    :parameters taskList: A List of task ids which is individually rendered into the HTML content
    :return: returns the HTML content to display on the page
    :rtype: String (of HTML content).
    """
    s = '<h1 id="achievements-title">Achievements</h1><ul id="achievements-list">'
    for task in taskList:
        if check_completed(task['taskId'], currentUserId):
            s += '''
                <li>
                <div class="achievement-head">
                <div class="achievement-left">
                <img class="achievement-badge-img" src="static/img/completed-achievement.png" height=46px>
                </div>
                <div class="achievement-right">
                <div class="achievement-title-container"><p class="achievement-titles">'''+ task['title'] +'''</p></div>
                </div>
                </div>
                </li>
            '''
        else:
            answerList = get_answers(task['taskId'])

            answerHTML = ""
            for answer in answerList:
                answerHTML += '<div class="achievement-answer-button" onclick="answerButtonClicked(this)">' + answer['answer'] + '</div>'

            s += '''<li>
                <div class="achievement-head incomplete">
                  <div class="achievement-left incomplete">
                    <img class="achievement-badge-img" src="static/img/empty-achievement.png" height=46px>
                  </div>
                  <div class="achievement-right incomplete" onclick="achievementQButtonPressed(this)">
                    <div class="achievement-title-container incomplete"><p class="achievement-titles incomplete">'''+ task['title'] +'''</p></div>
                  </div>
                  <div class="quiz-dropdown">
                    <p class="achievement-question-txt">'''+ task['description'] + '''</p>
                    '''+ answerHTML + '''
                  </div>
                </div>
              </li>'''
    s += '</ul>'
    return s

    def get_old_tasks(teamid):
        """
        Gets the task ids for the tasks for the building that have already been visited - these are still
        available for the user to complete
        :parameter teamid: A session variable, will be passed into the function based on who is logged into the system
        :return: Returns the task ids for the achievements associated with the visited buildings
        :rtype: List (list of int).
        """
        cur = mysql.connection.cursor()
        cur.execute(''' SELECT buildingId FROM visited WHERE teamId=%d; ''' %teamid)
        building = cur.fetchall()
        task = []
        for x in building:
            b = x['buildingId']
            cur.execute(''' SELECT taskId FROM Task WHERE buildingId=%d AND required=0; ''' %b)
            t = cur.fetchall()
            for ts in t:
                task.append(ts['taskId'])
        return task