# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

## TODO: change to form submit to ajax callback
def index():
    print '[INFO] form controller index...'
    print request.vars
    print session
    
    # trucate all data - only for dev/test
    truncateAllTables()
    
    return dict()


def saveEvidenceTypeQuestions():
    print '[INFO] form controller saveEvidenceTypeQuestions...'
    print request.vars

    crQsCodes = ["cr-ae", "cr-pr", "cr-ep"]
    ctQsCodes = ["ct-gr", "ct-pgd", "ct-pk", "ct-ph", "ct-gt"]
    expMbQsCodes = ["exp-m-st", "exp-m-at", "exp-m-mi"]
    expTsQsCodes = ["exp-t-st", "exp-t-at", "exp-t-tp"]
    
    if request.vars:
        ev_type = request.vars.evidencetype
        task_id = request.vars.task_id

        ev_form_id = db.evidence_type_form.insert(is_started=True, is_finished=False)

        if ev_type == "DDI clinical trial":
            insertQuestionsByCodes(ctQsCodes, qsMap, request.vars, ev_form_id)
        
        elif ev_type == "Case Report":
            insertQuestionsByCodes(crQsCodes, qsMap, request.vars, ev_form_id)

        elif ev_type == "Metabolic Experiment":
            insertQuestionsByCodes(expMbQsCodes, qsMap, request.vars, ev_form_id)

        elif ev_type == "Transport Experiment":
            insertQuestionsByCodes(expTsQsCodes, qsMap, request.vars, ev_form_id)
        else:
            print "[ERROR] evidence type undefined (%s)" % ev_type

        db.evidence_type.insert(task_id=task_id, participant=session.participant, mp_method=ev_type, evidence_type_form_id=ev_form_id, is_started=True, is_finished=False)
        
        printTables()

        # evidence type inference
        inferred_evidence_type = getInferredEvType()
        r = 'jQuery("#inferred-evidencetype").val("%s")' % inferred_evidence_type
        return r


# insert question and answer to evidence_type_question table
def insertQuestionsByCodes(codes, qsMap, data, ev_form_id):
    for code in codes:
        if code in qsMap:
            question, answer  = qsMap[code], data[code]
            
            if question and answer:
                print ev_form_id, question, answer
                db.evidence_type_question.insert(evidence_type_form_id=ev_form_id, question=question, answer=answer)


# send sparql query to virtuoso endpoint for specific evidence type inference
def getInferredEvType():
    inferred_evidence_type = "Demo inferred evidence type"
    return inferred_evidence_type
    

# truncate all tables in database
def truncateAllTables():

    db.evidence_type.truncate()
    db.evidence_type_form.truncate()
    db.evidence_type_question.truncate()


def printTables():
    # print db.executesql('SELECT * FROM participant_task;')    
    print db.executesql('SELECT * FROM evidence_type;')
    print db.executesql('SELECT * FROM evidence_type_form;')
    print db.executesql('SELECT * FROM evidence_type_question;')


