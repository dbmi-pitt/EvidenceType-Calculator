# -*- coding: utf-8 -*-
def index():
    print '[INFO] default controller index...'

    participants = getParticipants()
    print participants
    
    participant_options = []
    for participant in participants:
        participant_options.append(OPTION(participant[0], _value=participant[0]))

    form = FORM('Participant: ', SELECT(_name='participant', *participant_options, _value='select', _onchange="ajax('taskCallback', ['participant'], ':eval');"))

    return dict(login_form = form, task_summary_table = "")


# update task summary table based on participant selection
def taskCallback():
    print '[INFO] default task callback...'
    print request.vars

    tasks = getTasksByParticipant(request.vars.participant)
    table = "<table class='table'><tr><td>participant</td><td>task</td><td>with assist? (T=Yes, F=No)</td><td>is started</td><td>is finished</td><td>link</td></tr>"
    rows= ""
    
    # get summary table contents if valid participant is selected
    if request.vars.participant and request.vars.participant != "select":
        session.participant = request.vars.participant
        
        for task in tasks:
            rows += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td><a href='%s'>%s<a></td></tr>" % (task[0], task[1], task[2], task[3], task[4], URL(request.application, 'forms', 'index', vars=dict(task_id=task[1])), "task " + str(task[1]))
        
    table += rows + "</table>"

    r = 'jQuery("#summary_table").html("%s")' % table
    return r


# jump to evidence question form
def redirectToForm():
    redirect(URL(request.application, 'forms', 'index'))

    
# get all tasks assigned to the participant
# return list of tasks (participant, task_id, is assist, is started, is_finished)
def getTasksByParticipant(participant):
    # sql = "SELECT participant, task_id, assist FROM participant_task WHERE participant='%s';" % participant
    sql = "SELECT p.participant, p.task_id, p.assist, e.is_started, e.is_finished FROM participant_task p LEFT JOIN evidence_type e ON p.participant=e.participant AND p.task_id = e.task_id WHERE p.participant='%s';" % (participant)
    print "[DEBUG] get tasks by participant: " + sql
    return db.executesql(sql)


# get list of participants
def getParticipants():
    participants = db.executesql("SELECT distinct participant FROM participant_task;")
    return participants




