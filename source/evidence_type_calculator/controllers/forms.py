# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

def index():
    print '[INFO] controller form index...'
    
    # trucate all data - only for dev/test
    truncateAllTables()

    qsMap = {"ct-gr": "Group Randomization?", "ct-pgd": "Parallel Group Design?", "ct-pk": "Study Focused on Pharmacokinetic Processes?", "ct-ph": "Phenotyping?", "ct-gt": "Genotyping?", "cr-ae": "Reporting an adverse event?", "cr-pr": "Publically reported?", "cr-ep": "Following an evaluation protocol?", "exp-m-st": "Subtype?", "exp-m-at": "Assay Type?", "exp-m-mi": "Metabolic Inhibitor?", "exp-t-st": "Subtype?", "exp-t-at": "Assay Type?", "exp-t-tp": "Transporter Protein?"}
    user = "Ivan"

    crQsCodes = ["cr-ae", "cr-pr", "cr-ep"]
    ctQsCodes = ["ct-gr", "ct-pgd", "ct-pk", "ct-ph", "ct-gt"]
    expMbQsCodes = ["exp-m-st", "exp-m-at", "exp-m-mi"]
    expTsQsCodes = ["exp-t-st", "exp-t-at", "exp-t-tp"]

    print request.vars    

    if request.vars:
        evidence_type = request.vars.evidencetype
        ev_form_id = db.evidence_type_form.insert(is_started=True, is_finished=False)        

        if evidence_type == "DDI clinical trial":
            insertQuestionsByCodes(ctQsCodes, qsMap, request.vars, ev_form_id)
        
        elif evidence_type == "Case Report":
            insertQuestionsByCodes(crQsCodes, qsMap, request.vars, ev_form_id)

        elif evidence_type == "Metabolic Experiment":
            insertQuestionsByCodes(expMbQsCodes, qsMap, request.vars, ev_form_id)

        elif evidence_type == "Transport Experiment":
            insertQuestionsByCodes(expTsQsCodes, qsMap, request.vars, ev_form_id)
        else:
            print "[ERROR] evidence type undefined (%s)" % evidence_type
        
        printTables()

        # evidence type inference
        inferred_evidence_type = evidenceTypeInference()

        return dict(message = "Evidence type questions submit!", inferred_evidence_type = inferred_evidence_type, login_form="", task_summary_table="")
    
    return dict(inferred_evidence_type="")


# insert question and answer to evidence_type_question table
def insertQuestionsByCodes(codes, qsMap, data, ev_form_id):
    for code in codes:
        if code in qsMap:
            question, answer  = qsMap[code], data[code]
            
            if question and answer:
                db.evidence_type_question.insert(evidence_type_form_id=ev_form_id, question=question, answer=answer)


# send sparql query to virtuoso endpoint for specific evidence type inference
def evidenceTypeInference():

    inferred_evidence_type = "Specific clinical trial"
    return inferred_evidence_type
    


# truncate all tables in database
def truncateAllTables():

    db.evidence_type.truncate()
    db.evidence_type_form.truncate()
    db.evidence_type_question.truncate()


def printTables():
    print db.executesql('SELECT * FROM participant_task;')    
    print db.executesql('SELECT * FROM evidence_type;')
    print db.executesql('SELECT * FROM evidence_type_form;')
    print db.executesql('SELECT * FROM evidence_type_question;')


