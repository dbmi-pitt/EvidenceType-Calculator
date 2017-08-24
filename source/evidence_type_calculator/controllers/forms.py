# -*- coding: utf-8 -*-

def index():

    response.flash = T("test")
    return dict(message=T('evidence type form!'))


def evidenceTypeQuestions():
    
    print '[INFO] controller evidenceTypeQuestions...'
    
    # trucate all data - only for dev/test
    truncateAllTables()

    qsMap = {"ct-gr": "Group Randomization?", "ct-pgd": "Parallel Group Design?", "ct-pk": "Study Focused on Pharmacokinetic Processes?", "ct-ph": "Phenotyping?", "ct-gt": "Genotyping?", "cr-ae": "Reporting an adverse event?", "cr-pr": "Publically reported?", "cr-ep": "Following an evaluation protocol?"}
    user = "Ivan"

    crQsCodes = ["cr-ae", "cr-pr", "cr-ep"]
    ctQsCodes = ["ct-gr", "ct-pgd", "ct-pk", "ct-ph", "ct-gt"]

    print request.vars    
    evidence_type = request.vars.evidencetype

    ev_form_id = db.evidence_type_form.insert(is_started=True, is_finished=False)    
    ev_type_id = db.evidence_type.insert(document_id=1, participant=user, method=evidence_type, is_started=True, evidence_type_form_id = ev_form_id)

    if evidence_type == "DDI Clinical trial":
        insertQuestionsByCodes(ctQsCodes, qsMap, request.vars, ev_form_id)
        
    elif evidence_type == "Case Report":
        insertQuestionsByCodes(crQsCodes, qsMap, request.vars, ev_form_id)

    printTables()    
    return dict(message=T('Evidence type questions submit!'))


# insert question and answer to evidence_type_question table
def insertQuestionsByCodes(codes, qsMap, data, ev_form_id):
    for code in codes:
        if code in qsMap:
            question, answer  = qsMap[code], data[code]
            # print code, question, answer
            
            if question and answer:
                db.evidence_type_question.insert(evidence_type_form_id=ev_form_id, question=question, answer=answer)    


# truncate all tables in database
def truncateAllTables():

    db.evidence_type.truncate()
    db.evidence_type_form.truncate()
    db.evidence_type_question.truncate()


def printTables():
    
    print db.executesql('SELECT * FROM evidence_type;')
    print db.executesql('SELECT * FROM evidence_type_form;')
    print db.executesql('SELECT * FROM evidence_type_question;')
