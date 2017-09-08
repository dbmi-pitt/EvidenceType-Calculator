# -*- coding: utf-8 -*-
def index():
    print '[INFO] summary controller index...'
    
    # truncate all data - only for dev/test
    truncateAllTables()
    
    participants = getParticipants()
    
    participant_options = []
    for participant in participants:
        participant_options.append(OPTION(participant[0], _value=participant[0]))

    form = FORM('Participant: ', SELECT(_name='participant', *participant_options, _value='select', _onchange="ajax('getMyTask', ['participant'], ':eval');"))

    return dict(login_form = form, task_summary_table = "")


def getMyTask():
    print '[INFO] summary get my task...'
    print request.vars    
    session.part_code = request.vars.participant

    task = getNextTaskByParticipant(session.part_code)
    progress = getProgressForParticipant(session.part_code)
    
    print "[DEBUG] user (%s) task progress %s (%s)" % (session.part_code, progress["finished"], progress["total"])
    
    task_html = "<h5>Current progress: finisehd <span class='label label-default'>%s</span> &nbsp;&nbsp; total <span class='label label-default'>%s</span></h5><br>My next task:<br><br><table class='table'><tr><td>participant</td><td>task</td><td>with assist? (T=Yes, F=No)</td><td>link</td></tr>" % (progress["finished"], progress["total"])
    
    task_html += "<tr><td>%s</td><td>%s</td><td>%s</td><td><a href='%s'>%s<a></td></tr></table>" % (task["part_code"], task["task_id"], task["assist"], URL(request.application, 'forms', 'index', vars=dict(task_id=task["task_id"])), "task " + str(task["task_id"]))
    
    r = 'jQuery("#next_task_anchor").html("%s")' % task_html
    return r

    
# get next task for the participant
# return task (participant_code, task_id, is assist)
def getNextTaskByParticipant(part_code):
    sql = "SELECT p.participant, p.code, p.task_id, p.assist, e.is_started FROM participant_task p LEFT JOIN evidence_type e ON p.code=e.participant_code AND p.task_id = e.task_id WHERE p.code='%s' AND e.is_finished isnull ORDER BY p.task_id LIMIT 1;" % (part_code)
    print "[DEBUG] get tasks by participant: " + sql
    
    result = db.executesql(sql)
    if not result:
        return None    
    task = result[0]

    return {"part_code": task[1], "task_id": task[2], "assist": task[3]}


# get tasks progress for the participant
def getProgressForParticipant(part_code):
    finished = getFinshedCntForParticipant(part_code)[0]
    total = getTotalCntForParticipant(part_code)[0]

    return {"finished":finished, "total": total}


# get count of finished tasks for the participant
def getFinshedCntForParticipant(part_code):
    sql = "SELECT count(*) FROM participant_task p LEFT JOIN evidence_type e ON p.code=e.participant_code AND p.task_id = e.task_id WHERE p.code='%s' AND e.is_finished notnull;" % (part_code)
    return db.executesql(sql)[0]


# get total count of tasks for the participant
def getTotalCntForParticipant(part_code):
    sql = "SELECT count(*) FROM participant_task p LEFT JOIN evidence_type e ON p.code=e.participant_code AND p.task_id = e.task_id WHERE p.code='%s';" % (part_code)
    return db.executesql(sql)[0]    


# get list of participants
def getParticipants():
    participants = db.executesql("SELECT distinct code FROM participant_task;")
    return participants


# truncate all tables in database
def truncateAllTables():

    db.evidence_type_form.truncate()
    db.evidence_type_question.truncate()
    db.icl_form.truncate()
    db.icl_question.truncate()
    db.sub_method.truncate()
    db.evidence_type.truncate()
