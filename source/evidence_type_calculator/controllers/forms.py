# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
def index():
    print "[INFO] form controller index..."
    session.task_id = request.vars.task_id
    part_code = session.part_code
    
    print "participant (%s), task (%s)" % (part_code, session.task_id)
    
    truncateAllTables() # trucate all data - only for dev/test
    return dict()


# save inferred evidence type
def saveInferred():
    print '[INFO] form controller save inferred evidence type...'
    print session
    
    db((db.evidence_type.participant_code == session.part_code) & (db.evidence_type.task_id == session.task_id)).update(inferred_evidence_type = request.vars["inferred-evidencetype"])

    r = '$("#agree-with-inferred-div").css("display","none");' # hide agree/disagree buttons

    # show following questions
    if session.mp_method == "Case Report":
        r+= '$("#cr-ic-questions-div").css("display","block");'
    elif session.mp_method == "DDI clinical trial":
        r+= '$("#ct-ic-questions-div").css("display","block");'
    elif session.mp_method == "Metabolic Experiment":
        r+= '$("#ex-mt-ic-questions-div").css("display","block");'
    elif session.mp_method == "Transport Experiment":
        r+= '$("#ex-tp-ic-questions-div").css("display","block");'
    else:
        print "[ERROR] evidence type undefined (%s)" % session.mp_method

    return r


# save inferred and entered evidence type
def saveEnteredAndInferred():
    print '[INFO] form controller save inferred and entered evidence type...'    

    db((db.evidence_type.participant_code == session.part_code) & (db.evidence_type.task_id == session.task_id)).update(inferred_evidence_type = request.vars["inferred-evidencetype"], entered_evidence_type = request.vars["entered-evidencetype"])
    
    r = '$("#agree-with-inferred-div").css("display","none");' # hide agree/disagree buttons
    
    # show following questions
    if session.mp_method == "Case Report":
        r+= '$("#cr-ic-questions-div").css("display","block");'
    elif session.mp_method == "DDI clinical trial":
        r+= '$("#ct-ic-questions-div").css("display","block");'
    elif session.mp_method == "Metabolic Experiment":
        r+= '$("#ex-mt-ic-questions-div").css("display","block");'
    elif session.mp_method == "Transport Experiment":
        r+= '$("#ex-tp-ic-questions-div").css("display","block");'
    else:
        print "[ERROR] evidence type undefined (%s)" % session.mp_method
    
    return r

    
# save evidence type questions
def saveEvidenceTypeQuestions():
    print '[INFO] form controller save evidence type questions...'
    print request.vars

    crQsCodes = ["cr-ae", "cr-pr", "cr-ep"]
    ctQsCodes = ["ct-gr", "ct-pgd", "ct-pk", "ct-ph", "ct-gt"]
    expMbQsCodes = ["exp-m-st", "exp-m-at", "exp-m-mi"]
    expTsQsCodes = ["exp-t-st", "exp-t-at", "exp-t-tp"]
    
    if request.vars:
        ev_type = request.vars.evidencetype
        session.mp_method = ev_type

        ev_form_id = db.evidence_type_form.insert(is_started=True, is_finished=False)

        if ev_type == "DDI clinical trial":
            insertEvQuestionsByCodes(ctQsCodes, request.vars, ev_form_id)
        
        elif ev_type == "Case Report":
            insertEvQuestionsByCodes(crQsCodes, request.vars, ev_form_id)

        elif ev_type == "Metabolic Experiment":
            insertEvQuestionsByCodes(expMbQsCodes, request.vars, ev_form_id)

        elif ev_type == "Transport Experiment":
            insertEvQuestionsByCodes(expTsQsCodes, request.vars, ev_form_id)
        else:
            print "[ERROR] evidence type undefined (%s)" % ev_type

        # create evidence_type when assist with inference
        db.evidence_type.insert(task_id=session.task_id, participant_code=session.part_code, mp_method=ev_type, evidence_type_form_id=ev_form_id, is_started=True, is_finished=False)
        
        printTables()

        # evidence type inference
        inferred_evidence_type = getInferredEvType()
        r = '$("#inferred-evidencetype-div").css("display","block");$("#agree-with-inferred-div").css("display","block");jQuery("#inferred-evidencetype").val("%s")' % inferred_evidence_type
        return r


# insert question and answer to evidence_type_question table
def insertEvQuestionsByCodes(ui_codes, data, ev_form_id):
    for code in ui_codes:
        if code in global_ev_qs_map:
            question, answer  = global_ev_qs_map[code], data[code]
            
            if question and answer:
                db.evidence_type_question.insert(evidence_type_form_id=ev_form_id, question=question, answer=answer)

# insert question and answer to icl_question table
def insertIcQuestionsByCodes(ui_codes, data, ic_form_id):
    for code in ui_codes:
        if code in global_ev_qs_map:
            question, answer  = global_ev_qs_map[code], data[code]
            
            if question and answer:
                print ic_form_id, question, answer
                db.icl_question.insert(icl_type_form_id=ic_form_id, question=question, answer=answer)    


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


