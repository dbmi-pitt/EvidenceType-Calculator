# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

def index():
    print '[INFO] default controller index...'

    participants = getParticipants()
    participant_options = []
    for participant in participants:
        participant_options.append(OPTION(participant[1], _value=participant[1]))

    form = FORM('Participant: ', SELECT(_name='participant', *participant_options, _value='select', _onchange="ajax('taskCallback', ['participant'], ':eval');"))

    return dict(login_form = form, task_summary_table = "")


def taskCallback():
    print '[INFO] default task callback...'
    print request.vars

    part_name = request.vars.participant
    tasks = getTasksByParticipant(part_name)

    table = "<table class='table'>"
    for task in tasks:
        table += "<tr><td>%s</td><td>%s</td><td>%s</td><td><a href='%s'>%s<a></td></tr>" % (task[1], task[3], task[9], URL('redirectToForm'), task[1])
    table += "</table>"

    r = 'jQuery("#summary_table").html("%s")' % table
    # print r
    return r
        
    


def redirectToForm():
    redirect(URL(request.application, 'forms', 'index'))


def getTasksByParticipant(participant):
    sql = "SELECT * FROM evidence_type WHERE participant='%s';" % participant
    print sql
    
    tasks = db.executesql(sql)

    # print tasks
    return tasks


def getParticipants():
    participants = db.executesql("SELECT * FROM participant_task;")
    return participants




