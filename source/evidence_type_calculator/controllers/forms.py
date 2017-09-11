# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
def index():
    print "[INFO] form controller index..."
    session.task_id = request.vars.task_id
    if not session.task_id or not session.part_code:
        print "[ERROR] participant code (%s) or task_id (%s) undefined!" % (session.part_code, session.task_id)
        return
    else:
        print "participant (%s), task (%s)" % (session.part_code, session.task_id)    

    # check if there is finished evidence type form or inclusion criteria form available to load 
    sql = "SELECT evf.id, icf.id FROM evidence_type e LEFT JOIN evidence_type_form evf ON e.evidence_type_form_id = evf.id LEFT JOIN icl_form icf ON e.icl_form_id = icf.id WHERE e.participant_code = '%s' AND e.task_id = '%s';" % (session.part_code, session.task_id)
    form_status_res = db.executesql(sql)
    
    print form_status_res
    if form_status_res:        
        ev_form_id, ic_form_id = form_status_res[0][0], form_status_res[0][1]
        print ev_form_id, ic_form_id
    
    return dict()

    
## save evidence type questions to table evidence_type_form, evidence_type_question
def saveEvidenceTypeQuestions():
    print '[INFO] form controller save evidence type questions...'
    print request.vars
    
    if request.vars:
        session.mp_method = request.vars.evidencetype

        ev_form_id = db.evidence_type_form.insert(is_started=True, is_finished=False)
        session.ev_form_id = ev_form_id
        saveEvidenceTypeQuestionsHelper(session.mp_method, request.vars, ev_form_id)

        # create evidence_type when assist with inference
        db.evidence_type.insert(task_id=session.task_id, participant_code=session.part_code, mp_method=session.mp_method, evidence_type_form_id=ev_form_id, is_started=True, is_finished=False)    

        # evidence type inference
        inferred_evidence_type = getInferredEvType()
        
        r = '$("#inferred-evidencetype-div").css("display","block");$("#agree-with-inferred-div").css("display","block");jQuery("#inferred-evidencetype").val("%s");$("#calculate").hide();' % inferred_evidence_type
        return r

    
def saveEvidenceTypeQuestionsHelper(mp_method, data, ev_form_id):
    if mp_method == "DDI clinical trial":
        insertEvQuestionsByCodes(global_ct_ev_qs_codes, data, ev_form_id)        
    elif mp_method == "Case Report":
        insertEvQuestionsByCodes(global_cr_ev_qs_codes, data, ev_form_id)        
    elif mp_method == "Metabolic Experiment":
        insertEvQuestionsByCodes(global_ex_mt_ev_qs_codes, data, ev_form_id)        
    elif mp_method == "Transport Experiment":
        insertEvQuestionsByCodes(global_ex_tp_ev_qs_codes, data, ev_form_id)
    else:
        print "[ERROR] evidence type undefined (%s)" % mp_method


def insertEvQuestionsByCodes(ui_codes, data, ev_form_id):
    for code in ui_codes:
        if code in global_ev_qs_map:
            question, answer  = global_ev_qs_map[code], data[code]
            
            if question and answer:
                db.evidence_type_question.insert(evidence_type_form_id=ev_form_id, question=question, answer=answer)

                
# save inferred evidence type and show inclusion criteria questions
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


# save inferred and entered evidence type, show inclusion criteria questions
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
                

## save inclusion criteria questions to table icl_form, icl_question
def saveInclusionCriteriaQuestions():
    print '[INFO] form controller save inclusion criteria questions...'
    print request.vars
    session.mp_method = request.vars.evidencetype

    ic_form_id = db.icl_form.insert(is_started=True, is_finished=False)
    session.ic_form_id = ic_form_id
    
    saveInclusionCriteriaQuestionsHelper(session.mp_method, request.vars, ic_form_id)
    
    db((db.evidence_type.participant_code == session.part_code) & (db.evidence_type.task_id == session.task_id)).update(icl_form_id = ic_form_id)

    # get inclusion criteria result    
    ic_result_str = "No"
    ic_result = getInclusionCriteriaResult()
    if ic_result:
        ic_result_str = "Yes"
        
    db((db.evidence_type.participant_code == session.part_code) & (db.evidence_type.task_id == session.task_id)).update(is_meet_inclusion_criteria = ic_result)
    
    r = '$("#ic-div").css("display","block");$("#agree-with-ic-div").css("display","block");jQuery("#ic-result").val("%s");$("#calculate").hide();' % ic_result_str
    return r


def saveInclusionCriteriaQuestionsHelper(mp_method, data, ic_form_id):
    if mp_method == "DDI clinical trial":
        insertIcQuestionsByCodes(global_ct_ic_qs_codes, data, ic_form_id)        
    elif mp_method == "Case Report":
        insertIcQuestionsByCodes(global_cr_ic_qs_codes, data, ic_form_id)        
    elif mp_method == "Metabolic Experiment":
        insertIcQuestionsByCodes(global_ex_mt_ic_qs_codes, data, ic_form_id)        
    elif mp_method == "Transport Experiment":
        insertIcQuestionsByCodes(global_ex_tp_ic_qs_codes, data, ic_form_id)
    else:
        print "[ERROR] evidence type undefined (%s)" % mp_method
    
                
def insertIcQuestionsByCodes(ui_codes, data, ic_form_id):
    for code in ui_codes:
        if code in global_ic_qs_map:
            question, answer  = global_ic_qs_map[code], data[code]
            
            if question and answer:
                db.icl_question.insert(icl_form_id=ic_form_id, question=question, answer=answer)    


# send sparql query to virtuoso endpoint for specific evidence type inference
def getInferredEvType():
    inferred_evidence_type = "Demo inferred evidence type"
    return inferred_evidence_type


def getInclusionCriteriaResult():
    return True


def agreeInclusionCriteria():
    print '[INFO] form controller agree inclusion criteria...'
    db((db.evidence_type.participant_code == session.part_code) & (db.evidence_type.task_id == session.task_id)).update(is_agree_with_ic_result = True)


def disagreeInclusionCriteria():
    print '[INFO] form controller disagree inclusion criteria...'
    db((db.evidence_type.participant_code == session.part_code) & (db.evidence_type.task_id == session.task_id)).update(is_agree_with_ic_result = False)


# finished current task, redirect to summary page, mark the finished status
def finishTask():
    print '[INFO] form controller finish task...'
    db(db.icl_form.id == session.ic_form_id).update(is_finished = True)
    
    db((db.evidence_type.participant_code == session.part_code) & (db.evidence_type.task_id == session.task_id)).update(is_finished = True, disagree_comment = request.vars["ic-comment"])

    session.mp_method = None
    session.task_id = None
    session.ic_form_id = None
    
    redirect(URL(request.application, 'summary','index'), client_side=True)
    

