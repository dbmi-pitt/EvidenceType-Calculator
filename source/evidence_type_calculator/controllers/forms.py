# -*- coding: utf-8 -*-

import json
from SPARQLWrapper import SPARQLWrapper, JSON

SPARQL_HOST = '''http://localhost:8890/sparql'''
SPARQL_PREFIXES = '''
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX efo: <http://www.ebi.ac.uk/efo/>
'''
SPARQL_GRAPH = '''<http://www.semanticweb.org/rdb20/ontologies/2017/8/dikb-etypes-09222017#>'''
SPARQL_NO_RANDOMIZATION = '''
    ?gItem a owl:NegativePropertyAssertion;
              owl:sourceIndividual ?aItem;
              owl:targetIndividual obo:OBI_0302900. # an assay item is the source individual for a negative property assertion about group randomization   
'''
SPARQL_RANDOMIZATION = '''
    ?aItem obo:BFO_0000051 ?pItem. # has_part

    ?pItem a obo:OBI_0302900. # group randomization design
'''

SPARQL_PAR_GROUPS = '''
?aItem obo:BFO_0000055 ?rItem. # the assay realizes a design
?rItem a obo:BFO_0000017; 
     obo:RO_0000059 ?cItem. # the realizable entity concretizes a clinical study design 

?cItem a obo:OBI_0500001;
       obo:BFO_0000051 ?pItem. # the clinical study design has_part

?pItem a obo:OBI_0500006. # parallel group design
'''

SPARQL_PK = '''
?aItem obo:OBI_0000293 ?oItem1. # has specified input some organism 
?oItem1 a obo:OBI_0100026; # dideo:organism
             obo:RO_0000056 ?pItem1. # participates_in
?pItem1 a obo:DIDEO_00000052. # dideo:pharmacokinetic process
'''

SPARQL_PHENOTYPE = '''
?aItem obo:OBI_0000293 ?oItem2. # has specified input some organism 
?oItem2 a obo:OBI_0100026; # organism
       obo:RO_0000056 ?pItem2. # participates_in
?pItem2 a obo:ERO_0000923. # phenotype characterization
'''

SPARQL_GENOTYPE = '''
?aItem obo:OBI_0000293 ?oItem3. # has specified input some organism 
?oItem3 a obo:OBI_0100026; # organism
     obo:RO_0000056 ?gItem3. # participates_in
?gItem3 a efo:EFO_0000750. # genotype characterization
'''

SPARQL_EV_TYPE = '''
    ?evItem  a ?evType; # get all of the other evidence types this is classified as 
              obo:IAO_0000136 ?aItem.  # an evidence item defined using Cafe is about an assay item
 
    ?evType rdfs:label ?label.
'''


# this file is released under public domain and you can use without limitations
def index():
    print "[INFO] form controller index..."
    session.task_id = request.vars.task_id
    if not session.task_id or not session.part_code:
        print "[ERROR] participant code (%s) or task_id (%s) undefined!" % (session.part_code, session.task_id)
        return
    else:
        print "participant (%s), task (%s)" % (session.part_code, session.task_id)

    return dict()


# check if there is finished evidence type answers available to load 
def loadEvidenceTypeQuestions():
    sql1 = "SELECT evf.id, e.mp_method, e.inferred_evidence_type, e.is_agree_with_inference, e.entered_evidence_type FROM evidence_type e LEFT JOIN evidence_type_form evf ON e.evidence_type_form_id = evf.id WHERE e.participant_code = '%s' AND e.task_id = '%s';" % (session.part_code, session.task_id)
    result = db.executesql(sql1)
    
    if result:
        ev_form_id, mp_method, inferred_ev, agree_inferred, entered_ev = result[0][0], result[0][1], result[0][2], result[0][3], result[0][4]
        print "[INFO] load mp_method (%s), ev form (%s)" % (mp_method, ev_form_id)

        jsonData = {"mp_method": mp_method, "inferred_evidence_type": inferred_ev, "is_agree_with_inference": agree_inferred, "entered_evidence_type": entered_ev, "questions": {}}

        sql2 = "SELECT evq.ui_code, evq.answer FROM evidence_type_form evf JOIN evidence_type_question evq ON evf.id = evq.evidence_type_form_id WHERE evf.id = '%s'" % ev_form_id
        questions = db.executesql(sql2)
        
        for (code, answer) in questions:
            jsonData["questions"][code] = answer        
        return json.dumps(jsonData)


# check if there is finished inclusion criteria answers available to load 
def loadInclusionCriteriaQuestions(ic_form_id, mp_method):
    sql1 = "SELECT icf.id, e.mp_method, e.is_meet_inclusion_criteria, e.is_agree_with_ic_result, confidence, disagree_comment FROM evidence_type e LEFT JOIN icl_form icf ON e.icl_form_id = icf.id WHERE e.participant_code = '%s' AND e.task_id = '%s';" % (session.part_code, session.task_id)
    result = db.executesql(sql1)

    if result:
        ic_form_id, mp_method, ic_result, ic_agree, confidence, comment = result[0][0], result[0][1], result[0][2], result[0][3], result[0][4], result[0][5]
        print "[INFO] load mp_method (%s), ic form (%s)" % (mp_method, ic_form_id)

        jsonData = {"mp_method": mp_method, "is_meet_inclusion_criteria": ic_result, "is_agree_with_ic_result": ic_agree, "confidence": confidence, "disagree_comment": comment, "questions": {}}
        
        sql2 = "SELECT evq.ui_code, evq.answer FROM evidence_type_form evf JOIN evidence_type_question evq ON evf.id = evq.evidence_type_form_id WHERE evf.id = '%s'" % ev_form_id
        questions = db.executesql(sql2)
        
        for (code, answer) in questions:
            jsonData["questions"][code] = answer        
        return json.dumps(jsonData)

    
## save evidence type questions to table evidence_type_form, evidence_type_question
def saveEvidenceTypeQuestions():
    print '[INFO] form controller save evidence type questions'
    print request.vars
    
    if request.vars:
        session.mp_method = request.vars.evidencetype
        result = isEvidenceTypeFormExists()

        if not result: # task and form not exists
            ev_form_id = db.evidence_type_form.insert(is_started=True, is_finished=True)            
            session.ev_form_id = ev_form_id            
            saveEvidenceTypeQuestionsHelper(session.mp_method, request.vars, ev_form_id)

            # create evidence_type when assist with inference
            db.evidence_type.insert(task_id=session.task_id, participant_code=session.part_code, mp_method=session.mp_method, evidence_type_form_id=ev_form_id, is_started=True, is_finished=False)
        else: # task and form exists, just update questions
            ev_id, ev_form_id = result["id"], result["ev_form_id"]
            session.ev_form_id = ev_form_id
            session.mp_method = result["mp_method"]
            saveEvidenceTypeQuestionsHelper(session.mp_method, request.vars, ev_form_id)
            
            
        # evidence type inference
        inferred_evidence_type = getInferredEvType(request.vars)
        
        r = '$("#inferred-evidencetype-div").css("display","block");$("#agree-with-inferred-div").css("display","block");jQuery("#inferred-evidencetype").val("%s");$("#calculate").hide();' % inferred_evidence_type
        return r


def isEvidenceTypeFormExists():
    sql = "SELECT id, evidence_type_form_id, mp_method FROM evidence_type WHERE participant_code = '%s' AND task_id = '%s'" % (session.part_code, session.task_id)
    result = db.executesql(sql)
    print result
    if result:
        return {"id": result[0][0], "ev_form_id": result[0][1], "mp_method": result[0][2]}
    return None

    
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


# insert question if not exists, otherwise update the answer
def insertEvQuestionsByCodes(ui_codes, data, ev_form_id):
    for code in ui_codes:
        if code in global_ev_qs_map:
            question, answer  = global_ev_qs_map[code], data[code]            
            if question and answer:
                sql = "SELECT id FROM evidence_type_question WHERE evidence_type_form_id = '%s' and ui_code = '%s'" % (ev_form_id, code)
                result = db.executesql(sql)
                if result:
                    ev_question_id = result[0][0]
                    db(db.evidence_type_question.id == int(ev_question_id)).update(answer=answer)
                else:                
                    db.evidence_type_question.insert(evidence_type_form_id=ev_form_id, ui_code=code, question=question, answer=answer)

                
# save inferred evidence type
# show inclusion criteria questions
def agreeInferred():
    print '[INFO] form controller save inferred evidence type...'
    
    db((db.evidence_type.participant_code == session.part_code) & (db.evidence_type.task_id == session.task_id)).update(inferred_evidence_type = request.vars["inferred-evidencetype"], is_agree_with_inference = True)

    # hide agree/disagree buttons, show inclusion criteria form
    r = '$("#agree-with-inferred-div").css("display","none");showInclusionCriteriaByMethod("'+session.mp_method+'");' 
    return r


# save inferred and entered evidence type
# show inclusion criteria questions
def saveEnteredAndInferred():
    print '[INFO] form controller save inferred and entered evidence type...'    

    db((db.evidence_type.participant_code == session.part_code) & (db.evidence_type.task_id == session.task_id)).update(inferred_evidence_type = request.vars["inferred-evidencetype"], entered_evidence_type = request.vars["entered-evidencetype"], is_agree_with_inference = False)
    
    # hide agree/disagree buttons, show inclusion criteria form
    r = '$("#agree-with-inferred-div").css("display","none");showInclusionCriteriaByMethod("'+session.mp_method+'");'    
    return r
                

## save inclusion criteria questions to table icl_form, icl_question
def saveInclusionCriteriaQuestions():
    print '[INFO] form controller save inclusion criteria questions...'
    print request.vars
    session.mp_method = request.vars.evidencetype

    ic_form_id = db.icl_form.insert(is_started=True, is_finished=True)
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
                db.icl_question.insert(icl_form_id=ic_form_id, ui_code=code, question=question, answer=answer)    

# send sparql query to virtuoso endpoint for specific evidence type inference
def getInferredEvType(data):
    print "data as received by getInferredEvType: %s" % str(data)

    # set RDF store connection
    tstore = SPARQLWrapper(SPARQL_HOST)

    # start building the evidence type query
    q = SPARQL_PREFIXES + '''
SELECT distinct ?evItem ?evType ?label
FROM ''' + SPARQL_GRAPH + '''
WHERE {
    ?aItem a obo:OBI_0000070. # a study assay
'''

    # randomization?
    if data['ct-ev-question-1'] == 'yes':
        q = q + SPARQL_RANDOMIZATION
    elif data['ct-ev-question-1'] == 'no':
        q = q + SPARQL_NO_RANDOMIZATION

    # parallel group design? -- TODO: as defined, there will be no types with both group randomziation AND a parallel groups design. Should we make the q1 and q2 radio buttons work so that users can't select that option
    if data['ct-ev-question-2'] == 'yes':
        q = q + SPARQL_PAR_GROUPS

    # examining pharmacokinetics?
    if data['ct-ev-question-3'] == 'yes':
        q = q + SPARQL_PK

    # phenotyping done as part of the study?
    if data['ct-ev-question-4'] == 'yes':
        q = q + SPARQL_PHENOTYPE

    # genotyping done as part of the study?
    if data['ct-ev-question-5'] == 'yes':
        q = q + SPARQL_GENOTYPE
    
    # close the query with a request for the matching evidence types 
    q = q + SPARQL_EV_TYPE + '''
}
'''
    print q
    tstore.setQuery(q)
    tstore.setReturnFormat(JSON)
    qr = tstore.query().convert()    
    if len(qr["results"]["bindings"]) == 0:
        print "results from sparql query is none "
    else:
        print "results: %s" % qr
    
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
