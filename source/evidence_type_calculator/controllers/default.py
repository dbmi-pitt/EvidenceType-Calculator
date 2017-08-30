# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

def index():
    print '[INFO] default controller index...'

    participants = getParticipants()
    print participants
    
    participant_options = []
    for participant in participants:
        participant_options.append(OPTION(participant[0], _value=participant[0]))

    form = FORM('Participant: ', SELECT(_name='participant', *participant_options, _value='select', _onchange="ajax('default/taskCallback', ['participant'], ':eval');"))

    return dict(login_form = form, task_summary_table = "")


def taskCallback():
    print '[INFO] default task callback...'
    print request.vars

    part_name = request.vars.participant
    tasks = getTasksByParticipant(part_name)
    # print tasks

    table = "<table class='table'><tr><td>participant</td><td>task</td><td>with assist? (T=Yes, F=No)</td><td>link</td></tr>"
    for task in tasks:
        table += "<tr><td>%s</td><td>%s</td><td>%s</td><td><a href='%s'>%s<a></td></tr>" % (task[0], task[1], task[2], URL('redirectToForm'), task[1])
    table += "</table>"

    r = 'jQuery("#summary_table").html("%s")' % table
    # print r
    return r


# jump to form
def redirectToForm():
    redirect(URL(request.application, 'forms', 'index'))

    
# get all tasks assigned to the participant
def getTasksByParticipant(participant):
    sql = "SELECT participant, task_id, assist FROM participant_task WHERE participant='%s';" % participant
    tasks = db.executesql(sql)
    return tasks


# get list of participants
def getParticipants():
    participants = db.executesql("SELECT distinct participant FROM participant_task;")
    return participants




