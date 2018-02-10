# -*- coding: utf-8 -*-

import json
from SPARQLWrapper import SPARQLWrapper, JSON

### START SPARQL header
SPARQL_HOST = '''http://localhost:8890/sparql'''
SPARQL_PREFIXES = '''
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX efo: <http://www.ebi.ac.uk/efo/>
'''
# SPARQL_GRAPH = '''<http://www.semanticweb.org/rdb20/ontologies/2017/8/dikb-etypes-09222017#>'''
SPARQL_FROM_GRAPH = '''FROM <http://www.semanticweb.org/rdb20/ontologies/2018/1/dikb-etypes-0206018#>
FROM <http://purl.obolibrary.org/obo/dideo.owl#>'''

### END SPARQL header

### START retrieve evidence types (this goes AFTER the other parts specific to clinical trials, case reports, and experiements)
SPARQL_EV_TYPE = '''

    ?evItem  a ?evType;             # get all of the other evidence types this is classified as 
           obo:IAO_0000136 ?aItem.  # an evidence item is about the assay item ?aItem
    ?evType rdfs:label ?label;            # get the evidence type label... 
            obo:IAO_0000115 ?definition.  # ...and definition(s)

    FILTER NOT EXISTS {
      ?evItem a ?z.
      ?z rdfs:subClassOf ?evType.
   }

'''
### END retrieve evidence types

### START of case report instance query parts
SPARQL_OBSERVATIONAL_REPORT = '''
    ?aItem obo:RO_0002404 ?pItem. # causally downstream of some occurrent
    ?pItem a obo:BFO_0000003.
'''

SPARQL_ADVERSE_EVENT = '''
     # the occurrent IS an adverse event
     ?pItem a obo:OAE_0000005.
'''

SPARQL_NOT_ADVERSE_EVENT = '''
     # the occurrent is NOT an adverse drug event
    FILTER NOT EXISTS {
      ?pItem a obo:OAE_0000005.
    }    
'''

SPARQL_PRECEDED_BY_DRUG_ADMIN = '''
    ?pItem obo:BFO_0000062 ?da. # preceded by drug administration 
    ?da a obo:DRON_00000031.
'''

SPARQL_NOT_PRECEDED_BY_DRUG_ADMIN = '''
   FILTER NOT EXISTS {
     ?pItem obo:BFO_0000062 ?da. # preceded by drug administration 
     ?da a obo:DRON_00000031.
   }
'''

SPARQL_DDI_ROLES = '''
    ?da obo:RO_0000057 ?d1.   # the drug administration has participant some entity that is the bearer of an object drug role
    ?d1 obo:RO_0000053 ?oRole.
    ?oRole a obo:DIDEO_00000012. 
    
    ?da obo:RO_0000057 ?d2.   # the drug administration has participant some entity that is the bearer of a precipitant drug role
    ?d2 obo:RO_0000053 ?precRole.
    ?precRole a obo:DIDEO_00000013.
'''

SPARQL_NOT_DDI_ROLES = '''
  FILTER NOT EXISTS {
     ?da obo:RO_0000057 ?d1.   # the drug administration has participant some entity that is the bearer of an object drug role
     ?d1 obo:RO_0000053 ?oRole.
     ?oRole a obo:DIDEO_00000012. 
    
     ?da obo:RO_0000057 ?d2.   # the drug administration has participant some entity that is the bearer of a precipitant drug role
     ?d2 obo:RO_0000053 ?precRole.
     ?precRole a obo:DIDEO_00000013.
  }
'''

SPARQL_REPORT_IN_PUBLIC_DATABASE = '''
    ?eice a obo:DIDEO_00000053;  # evidence information content entity
       obo:IAO_0000136 ?aItem;   # is about the assay 
       obo:BFO_0000050 ?prdb.  # is part of a public reporting database
    ?prdb a obo:DIDEO_00000082.
'''

SPARQL_REPORT_NOT_IN_PUBLIC_DATABASE = '''
  FILTER NOT EXISTS {
    ?eice a obo:DIDEO_00000053;  # evidence information content entity
       obo:IAO_0000136 ?aItem;   # is about the assay 
       obo:BFO_0000050 ?prdb.  # is part of a public reporting database
    ?prdb a obo:DIDEO_00000082.
  }
'''

SPARQL_REPORT_EVALUATED_FOR_CAUSALITY = '''
    ?eice a obo:DIDEO_00000053;  # evidence information content entity
       obo:IAO_0000136 ?aItem;   # is about the assay 
       obo:OBI_0000312 ?pp.  # is specified output of planned process that is an ADE causality evaluation protocol
    ?pp obo:BFO_0000055 ?re. # (realizes a realizable entity...)
    ?re obo:RO_0000059 ?adeep. # (...that concretizes a planned process...)
    ?adeep a obo:DIDEO_00000087. # (... that is an ADE causality evaluation protocol)
'''

SPARQL_REPORT_NOT_EVALUATED_FOR_CAUSALITY = '''
  FILTER NOT EXISTS {
    ?eice a obo:DIDEO_00000053;  # evidence information content entity
       obo:IAO_0000136 ?aItem;   # is about the assay 
       obo:OBI_0000312 ?pp.  # is specified output of planned process that is an ADE causality evaluation protocol
    ?pp obo:BFO_0000055 ?re. # (realizes a realizable entity...)
    ?re obo:RO_0000059 ?adeep. # (...that concretizes a planned process...)
    ?adeep a obo:DIDEO_00000087. # (... that is an ADE causality evaluation protocol)
  }
'''
### END of case report instance query parts

### START of clinical trial instance query parts
SPARQL_RANDOMIZATION = '''
    ?aItem obo:BFO_0000051 ?pItem. # has_part
    ?pItem a obo:OBI_0302900. # group randomization design
'''

SPARQL_NO_RANDOMIZATION = '''
   ?gItem a owl:NegativePropertyAssertion;
           owl:sourceIndividual ?aItem;
           owl:targetIndividual obo:OBI_0302900. # an assay item is the source individual for a negative property assertion about group randomization
'''

SPARQL_PAR_GROUPS = '''

   ?aItem obo:BFO_0000055 ?rItem. # the assay realizes a design
   ?rItem a obo:BFO_0000017; 
       obo:RO_0000059 ?cItem. # the realizable entity concretizes a clinical study design 
   ?cItem a obo:OBI_0500001;
       obo:BFO_0000051 ?pItem. # the clinical study design has_part
   ?pItem a obo:OBI_0500006. # parallel group design

'''

SPARQL_NOT_PAR_GROUPS = '''

 FILTER NOT EXISTS { 
   ?aItem obo:BFO_0000055 ?rItem. # the assay realizes a design
   ?rItem a obo:BFO_0000017; 
      obo:RO_0000059 ?cItem. # the realizable entity concretizes a clinical study design 
   ?cItem a obo:OBI_0500001;
     obo:BFO_0000051 ?pItem. # the clinical study design has_part
   ?pItem a obo:OBI_0500006. # parallel group design
 }

'''

SPARQL_PK = '''

   ?aItem obo:OBI_0000293 ?dItem1. # has specified input some drug
   ?dItem1 a obo:CHEBI_24431. # CHEBI chemical entity

   ?aItem obo:OBI_0000293 ?oItem1. # has specified input some organism 
   ?oItem1 a obo:OBI_0100026; # dideo:organism
             obo:RO_0000056 ?pItem1. # participates_in
   ?pItem1 a obo:DIDEO_00000052. # dideo:pharmacokinetic process

'''

SPARQL_NOT_PK = '''

  ?aItem obo:OBI_0000293 ?dItem1. # has specified input some drug
  ?dItem1 a obo:CHEBI_24431. # CHEBI chemical entity

  ?aItem obo:OBI_0000293 ?dItem2.FILTER(?dItem1 != ?dItem2) # has specified input some other drug
  ?dItem2 a obo:CHEBI_24431. # CHEBI chemical entity
 
  FILTER NOT EXISTS {
   ?aItem obo:OBI_0000293 ?oItem1. # has specified input some organism 
   ?oItem1 a obo:OBI_0100026; # dideo:organism
             obo:RO_0000056 ?pItem1. # participates_in
   ?pItem1 a obo:DIDEO_00000052. # dideo:pharmacokinetic process
  } 

'''

SPARQL_PHENOTYPE = '''

  ?aItem obo:OBI_0000293 ?oItem2. # has specified input some organism 
  ?oItem2 a obo:OBI_0100026; # organism
        obo:RO_0000056 ?pItem2. # participates_in
  ?pItem2 a obo:ERO_0000923. # phenotype characterization

'''

SPARQL_NOT_PHENOTYPE = '''

FILTER NOT EXISTS {
 ?aItem obo:OBI_0000293 ?oItem2. # has specified input some organism 
 ?oItem2 a obo:OBI_0100026; # organism
       obo:RO_0000056 ?pItem2. # participates_in
 ?pItem2 a obo:ERO_0000923. # phenotype characterization
}

'''

SPARQL_GENOTYPE = '''

?aItem obo:OBI_0000293 ?oItem3. # has specified input some organism 
?oItem3 a obo:OBI_0100026; # organism
     obo:RO_0000056 ?gItem3. # participates_in
?gItem3 a efo:EFO_0000750. # genotype characterization

'''

SPARQL_NOT_GENOTYPE = '''

FILTER NOT EXISTS {
?aItem obo:OBI_0000293 ?oItem3. # has specified input some organism 
?oItem3 a obo:OBI_0100026; # organism
     obo:RO_0000056 ?gItem3. # participates_in
?gItem3 a efo:EFO_0000750. # genotype characterization
}

'''
### END of clinical trial instance query parts

### START of in vitro metabolism experiments
SPARQL_IN_VITRO_DESIGN = '''
    ?aItem obo:BFO_0000055 ?re. # assay realizes a realizable entity...
    ?re obo:RO_0000059 ?ivd. # ...that concretizes an entity
    ?ivd a obo:OBI_0001285. # ... that is an in vitro study design
'''

SPARQL_NOT_IN_VITRO_DESIGN = '''
  NOT EXISTS {
    ?aItem obo:BFO_0000055 ?re. # assay realizes a realizable entity...
    ?re obo:RO_0000059 ?ivd. # ...that concretizes an entity
    ?ivd a obo:OBI_0001285. # ... that is an in vitro study design
  }
'''

SPARQL_METABOLISM_IDENTIFICATION = '''
    ?aItem obo:OBI_0000293 ?dItem1. # has specified input some ?dItem1
    ?dItem1 a obo:CHEBI_24431; # ?dItem1 a CHEBI chemical entity
         obo:BFO_0000050 ?dp;  # part of ?dp
         obo:RO_0000056  ?mp.  # participates in ?mp
    ?dp a obo:DRON_00000005. # ?dp is a drug product
    ?mp a obo:GO_0008152.   # ?mp is a metabolic process 
'''

SPARQL_NOT_METABOLISM_IDENTIFICATION = '''
  FILTER NOT EXISTS {
    ?aItem obo:OBI_0000293 ?dItem1. # has specified input some ?dItem1
    ?dItem1 a obo:CHEBI_24431; # ?dItem1 a CHEBI chemical entity
         obo:BFO_0000050 ?dp;  # part of ?dp
         obo:RO_0000056  ?mp.  # participates in ?mp
    ?dp a obo:DRON_00000005. # ?dp is a drug product
    ?mp a obo:GO_0008152.   # ?mp is a metabolic process 
  }
'''

SPARQL_METABOLISM_INHIBITION = '''
    ?aItem obo:OBI_0000293 ?dItem1. # has specified input some ?dItem1
    ?dItem1 a obo:CHEBI_24431; # ?dItem1 a CHEBI chemical entity
         obo:BFO_0000050 ?dp;  # part of ?dp
         obo:RO_0000056  ?mp.  # participates in ?mp
    ?dp a obo:DRON_00000005. # ?dp is a drug product
    ?mp a obo:GO_0009892.  # ?mp is a negative regulation of metabolic process 
'''

SPARQL_NOT_METABOLISM_INHIBITION = '''
  FILTER NOT EXISTS {
    ?aItem obo:OBI_0000293 ?dItem1. # has specified input some ?dItem1
    ?dItem1 a obo:CHEBI_24431; # ?dItem1 a CHEBI chemical entity
         obo:BFO_0000050 ?dp;  # part of ?dp
         obo:RO_0000056  ?mp.  # participates in ?mp
    ?dp a obo:DRON_00000005. # ?dp is a drug product
    ?mp a obo:GO_0009892.  # ?mp is a negative regulation of metabolic process 
  }
'''

SPARQL_INVOLVES_CYP450 = '''
    ?mp obo:RO_0000057 ?cyp. # ?mp has participant some ?cyp 
    ?cyp a obo:CHEBI_38559.
'''

SPARQL_NOT_INVOLVES_CYP450 = '''
  FILTER NOT EXISTS { 
    ?mp obo:RO_0000057 ?cyp. # ?mp has participant some ?cyp 
    ?cyp a obo:CHEBI_38559.
  }
'''

SPARQL_INVOLVES_RECOMBINANT_SYSTEM = '''
   ?aItem obo:OBI_0000293 ?sysItem1. # has specified input some ?sysItem1
   ?sysItem1 a obo:CLO_0000031. # ?sysItem1 a cell line
'''

SPARQL_NOT_INVOLVES_RECOMBINANT_SYSTEM = '''
  FILTER NOT EXISTS {
   ?aItem obo:OBI_0000293 ?sysItem1. # has specified input some ?sysItem1
   ?sysItem1 a obo:CLO_0000031. # ?sysItem1 a cell line
  }
'''


SPARQL_INVOLVES_HUMAN_MICROSOMES = '''
   ?aItem obo:OBI_0000293 ?sysItem1. # has specified input some ?sysItem1
   ?sysItem1 a obo:OBI_0001479; # ?sysItem1 a tissue sample 
        obo:OBI_0000312 ?scp.   # ?sysItem1 a specified output of ?scp
   ?scp a obo:OBI_0000659; # ?scp is a specimen collection process
      obo:OBI_0000293 ?hs.   # ?scp has specified input ?hs 
   #?hs a obo:NCBITaxon_9606. # ?hs of type Homo Sapiens
'''

SPARQL_NOT_INVOLVES_HUMAN_MICROSOMES = '''
  FILTER NOT EXISTS {
   ?aItem obo:OBI_0000293 ?sysItem1. # has specified input some ?sysItem1
   ?sysItem1 a obo:OBI_0001479; # ?sysItem1 a tissue sample 
        obo:OBI_0000312 ?scp.   # ?sysItem1 a specified output of ?scp
   ?scp a obo:OBI_0000659; # ?scp is a specimen collection process
      obo:OBI_0000293 ?hs.   # ?scp has specified input ?hs 
   #?hs a obo:NCBITaxon_9606. # ?hs of type Homo Sapiens
 }
'''

SPARQL_INVOLVES_ANTIBODY_INHIBITOR = '''
   ?aItem obo:OBI_0000293 ?sysItem2. # has specified input some ?sysItem2
   ?sysItem2 a obo:GO_0042571;  # ?sysItem2 a immunoglobulin complex, circulating 
          obo:RO_0000053 ?role. # ?sysItem2 is the bearer of ?role
   ?role a obo:CHEBI_35222.     # ?role is an inhibitor
'''

SPARQL_NOT_INVOLVES_ANTIBODY_INHIBITOR = '''
 FILTER NOT EXISTS {
   ?aItem obo:OBI_0000293 ?sysItem2. # has specified input some ?sysItem2
   ?sysItem2 a obo:GO_0042571;  # ?sysItem2 a immunoglobulin complex, circulating 
          obo:RO_0000053 ?role. # ?sysItem2 is the bearer of ?role
   ?role a obo:CHEBI_35222.     # ?role is an inhibitor
 }
'''

SPARQL_INVOLVES_CHEMICAL_INHIBITOR = '''
   ?aItem obo:OBI_0000293 ?chemEnt. # has specified input some ?chemEnt
   ?chemEnt a obo:CHEBI_24431;  # ?chemEnt a chemical entity 
          rdf:type [owl:complementOf obo:GO_0042571]; # ?chemEnt is not a immunoglobulin complex, circulating 
          obo:RO_0000053 ?role. # ?chemEn is the bearer of ?role
   ?role a obo:CHEBI_35222.     # ?role is an inhibitor
'''

SPARQL_NOT_INVOLVES_CHEMICAL_INHIBITOR = '''
 FILTER NOT EXISTS {
   ?aItem obo:OBI_0000293 ?chemEnt. # has specified input some ?chemEnt
   ?chemEnt a obo:CHEBI_24431;  # ?chemEnt a chemical entity 
          rdf:type [owl:complementOf obo:GO_0042571]; # ?chemEnt is not a immunoglobulin complex, circulating 
          obo:RO_0000053 ?role. # ?chemEn is the bearer of ?role
   ?role a obo:CHEBI_35222.     # ?role is an inhibitor
 }
'''
### END of in vitro metabolism experiments

### START of in vitro transport experiments
SPARQL_EX_VIVO_DESIGN = '''
    ?aItem obo:BFO_0000055 ?re. # assay realizes a realizable entity...
    ?re obo:RO_0000059 ?ivd. # ...that concretizes an entity
    ?ivd a obo:OBI_0001211. # ... that is an ex vivo study design
'''

SPARQL_TRANSPORT_IDENTIFICATION = '''
    ?aItem obo:OBI_0000293 ?chemSubst1. # has specified input some ?chemSubst1
    ?chemSubst1 a obo:CHEBI_24431;      # ?chemSubst1 a CHEBI chemical entity
          obo:OBI_0000312 ?tp.          # is specified output of ?tp
    ?tp a obo:GO_0098739;               # ?tp is import across a plasma membrane
          obo:RO_0000057 ?pt;           # ?tp has participant some ?pt
          obo:RO_0000057 ?chemSubst2.   # ?tp has participant some ?chemSubst2
    ?pt a obo:CHEBI_36080.              # ?pt a protein
    ?chemSubst2 a obo:CHEBI_24431;      # ?chemSubst2 a CHEBI chemical entity
            obo:BFO_0000050 ?dp.        # part of ?dp    
    ?dp a obo:DRON_00000005.            # ?dp is a drug product
'''

SPARQL_TRANSPORT_INHIBITION = '''
   ?aItem obo:OBI_0000293 ?chemSubst1. # has specified input some ?chemSubst1
    ?chemSubst1 a obo:CHEBI_24431;      # ?chemSubst1 a CHEBI chemical entity
          obo:OBI_0000312 ?tp.          # is specified output of ?tp
    ?tp a obo:GO_0032410;               # ?tp is negative regulation of transporter activity
          obo:RO_0000057 ?pt;           # ?tp has participant some ?pt
          obo:RO_0000057 ?chemSubst2.   # ?tp has participant some ?chemSubst2
    ?pt a obo:CHEBI_36080.              # ?pt a protein
    ?chemSubst2 a obo:CHEBI_24431;      # ?chemSubst2 a CHEBI chemical entity
            obo:BFO_0000050 ?dp.        # part of ?dp    
    ?dp a obo:DRON_00000005.            # ?dp is a drug product
'''

SPARQL_OVEREXPRESSED_CELL_LINE = '''
    ?aItem obo:OBI_0000293 ?clc. # has specified input some ?clc
    ?clc a obo:CLO_0000001;      # ?clc a cell line cell
          obo:RO_0000056  ?ovx.  # ?clc participates in ?ovx
    ?ovx a obo:INO_0000114.      # ?ovx an overexpression 
'''

SPARQL_NOT_OVEREXPRESSED_CELL_LINE = '''
  FILTER NOT EXISTS {
    ?aItem obo:OBI_0000293 ?clc. # has specified input some ?clc
    ?clc a obo:CLO_0000001;      # ?clc a cell line cell
          obo:RO_0000056  ?ovx.  # ?clc participates in ?ovx
    ?ovx a obo:INO_0000114.      # ?ovx an overexpression 
  }
'''

SPARQL_CACO_2_CELL_LINE = '''
    ?aItem obo:OBI_0000293 ?cl. # has specified input some ?cl
    ?cl a obo:CLO_0002172.      # ?cl a Caco 2 cell
''' 

SPARQL_NOT_CACO_2_CELL_LINE = '''
  FILTER NOT EXISTS {
    ?aItem obo:OBI_0000293 ?cl. # has specified input some ?cl
    ?cl a obo:CLO_0002172.      # ?cl a Caco 2 cell
  }
''' 

SPARQL_OATP1B1 = '''
     ?pt a obo:PR_000015223. # ?pt is a solute carrier organic anion transporter family member 1B1
'''

SPARQL_NOT_OATP1B1 = '''
   FILTER NOT EXISTS {
     ?pt a obo:PR_000015223. # ?pt is a solute carrier organic anion transporter family member 1B1
   }
'''

SPARQL_OATP1B3 = '''
     ?pt a obo:PR_000015224. # ?pt is a solute carrier organic anion transporter family member 1B3
'''

SPARQL_NOT_OATP1B3 = '''
  FILTER NOT EXISTS {
     ?pt a obo:PR_000015224. # ?pt is a solute carrier organic anion transporter family member 1B3
  }
'''

SPARQL_P_GLYCOPROTEIN = '''
     ?pt a obo:PR_000001891. # ?pt is a multidrug resistance protein 1 (p-glycoprotein)  
'''

SPARQL_NOT_P_GLYCOPROTEIN = '''
  FILTER NOT EXISTS {
     ?pt a obo:PR_000001891. # ?pt is a multidrug resistance protein 1 (p-glycoprotein)  
  }
'''

### END of in vitro transport experiments


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
        ietTpl = getInferredEvType(request.vars)
        ietDefandNotes = ietTpl[1]
        if ietTpl[2] != "":
            ietDefandNotes += "<br><i>Notes:</i>" + ietTpl[2]
            
        r = '$("#inferred-evidencetype-div").css("display","block");$("#agree-with-inferred-div").css("display","block");jQuery("#inferred-evidencetype").val("%s");jQuery("#inferred-evidencetype-def").html("<i>Definition:</i> %s");$("#calculate").hide();' % (ietTpl[0], ietDefandNotes)

        return r


def isEvidenceTypeFormExists():
    sql = "SELECT id, evidence_type_form_id, mp_method FROM evidence_type WHERE participant_code = '%s' AND task_id = '%s'" % (session.part_code, session.task_id)
    result = db.executesql(sql)
    print result
    if result:
        return {"id": result[0][0], "ev_form_id": result[0][1], "mp_method": result[0][2]}
    return None

    
def saveEvidenceTypeQuestionsHelper(mp_method, data, ev_form_id):
    if mp_method == "Clinical study":
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
    if mp_method == "Clinical study":
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

    # notes to pass on to the user to help with explanations
    inferenceNotes = ""
    
    # set RDF store connection
    tstore = SPARQLWrapper(SPARQL_HOST)

    # start building the evidence type query
    q = SPARQL_PREFIXES + '''
SELECT distinct ?evItem ?evType ?label ?definition
''' + SPARQL_FROM_GRAPH + '''
WHERE {
    ?aItem a obo:OBI_0000070. # a study assay
'''

    if not data.get('cr-ev-question-1'):
        print "INFO: skipping case report questions"
    else:
        q = q + SPARQL_OBSERVATIONAL_REPORT
        
        # adverse drug event report?
        if data['cr-ev-question-1'] == 'yes':
            q = q + SPARQL_ADVERSE_EVENT + SPARQL_PRECEDED_BY_DRUG_ADMIN
        elif data['cr-ev-question-1'] == 'no':
            q = q + SPARQL_NOT_ADVERSE_EVENT + SPARQL_NOT_PRECEDED_BY_DRUG_ADMIN
        elif data['cr-ev-question-1'] == 'unsure':
            q = q + SPARQL_NOT_ADVERSE_EVENT + SPARQL_NOT_PRECEDED_BY_DRUG_ADMIN
            
        # Publicly (spontaneously) reported?
        if data['cr-ev-question-2'] == 'yes':
            q = q + SPARQL_REPORT_IN_PUBLIC_DATABASE
        elif data['cr-ev-question-2'] == 'no':
            q = q + SPARQL_REPORT_NOT_IN_PUBLIC_DATABASE

        # Involves a suspected drug-drug interaction?
        if data['cr-ev-question-4'] == 'yes':
            q = q + SPARQL_DDI_ROLES
        elif data['cr-ev-question-4'] == 'no':
            q = q + SPARQL_NOT_DDI_ROLES

        # Was an evaluation of adverse event causality conducted?
        if data['cr-ev-question-3'] == 'yes':
            q = q + SPARQL_REPORT_EVALUATED_FOR_CAUSALITY
        elif data['cr-ev-question-3'] == 'no':
            q = q + SPARQL_REPORT_NOT_EVALUATED_FOR_CAUSALITY
            
    if not data.get('ct-ev-question-1'):
        print "INFO: skipping clinical trial questions"
    else:
        # randomization?
        if data['ct-ev-question-1'] == 'yes':
            q = q + SPARQL_RANDOMIZATION
        elif data['ct-ev-question-1'] == 'no':
            q = q + SPARQL_NO_RANDOMIZATION

        # parallel group design? -- TODO: as defined, there will be no types with both group randomziation AND a parallel groups design. Should we make the q1 and q2 radio buttons work so that users can't select that option
        if data['ct-ev-question-2'] == 'yes':
            q = q + SPARQL_PAR_GROUPS

        elif data['ct-ev-question-2'] == 'no':
            q = q + SPARQL_NOT_PAR_GROUPS
            
        # examining pharmacokinetics?
        if data['ct-ev-question-3'] == 'yes':
            q = q + SPARQL_PK
            if data['ct-ev-question-1'] == 'yes':
                q = q.replace(SPARQL_RANDOMIZATION,'')
                inferenceNotes += " Randomization is currently ignored in the definition of pharmacokinetic studies. "
            elif data['ct-ev-question-1'] == 'no':
                q = q.replace(SPARQL_NO_RANDOMIZATION,'')
                inferenceNotes += " Randomization is currently ignored in the definition of pharmacokinetic studies. "    
        elif data['ct-ev-question-3'] == 'no':
            q = q + SPARQL_NOT_PK

        # phenotyping done as part of the study?
        if data['ct-ev-question-4'] == 'yes':
            q = q + SPARQL_PHENOTYPE
        elif data['ct-ev-question-4'] == 'no':
            q = q + SPARQL_NOT_PHENOTYPE

        # genotyping done as part of the study?
        if data['ct-ev-question-5'] == 'yes':
            q = q + SPARQL_GENOTYPE
        elif data['ct-ev-question-5'] == 'no':
            q = q + SPARQL_NOT_GENOTYPE

    if not data.get('ex-ev-mt-question-1'):
        print "INFO: skipping in vitro metabolic questions"
    else:
        q = q + SPARQL_IN_VITRO_DESIGN
        
        if data['ex-ev-mt-question-1'] == 'inhibition':
            q = q + SPARQL_METABOLISM_INHIBITION
        elif data['ex-ev-mt-question-1'] == 'identification':
            q = q + SPARQL_METABOLISM_IDENTIFICATION
        elif data['ex-ev-mt-question-1'] == 'unsure':
            q = q + SPARQL_NOT_METABOLISM_INHIBITION + SPARQL_NOT_METABOLISM_IDENTIFICATION

            
        if data['ex-ev-mt-question-4'] == 'yes':
            q = q + SPARQL_INVOLVES_CYP450
        elif data['ex-ev-mt-question-4'] == 'no':
            q = q + SPARQL_NOT_INVOLVES_CYP450
        elif data['ex-ev-mt-question-4'] == 'unsure':
            q = q + SPARQL_NOT_INVOLVES_CYP450

            
        if data['ex-ev-mt-question-2'] == 'humanTissue':
            q = q + SPARQL_INVOLVES_HUMAN_MICROSOMES
        elif data['ex-ev-mt-question-2'] == 'cellLine':
            q = q + SPARQL_INVOLVES_RECOMBINANT_SYSTEM
        elif data['ex-ev-mt-question-2'] == 'unsure':
            q = q  # Could be either so we can't use NOT

            
        if data['ex-ev-mt-question-3'] == 'antibody':
            q = q + SPARQL_INVOLVES_ANTIBODY_INHIBITOR
        elif data['ex-ev-mt-question-3'] == 'chemical':
            q = q + SPARQL_INVOLVES_CHEMICAL_INHIBITOR
        elif data['ex-ev-mt-question-3'] == 'none':
            q = q + SPARQL_NOT_INVOLVES_ANTIBODY_INHIBITOR + SPARQL_NOT_INVOLVES_CHEMICAL_INHIBITOR
        elif data['ex-ev-mt-question-3'] == 'unsure':
            q = q + SPARQL_NOT_INVOLVES_ANTIBODY_INHIBITOR + SPARQL_NOT_INVOLVES_CHEMICAL_INHIBITOR            
            
    if not data.get('ex-tp-ev-question-1'):
        print "INFO: skipping in vitro transport questions"
    else:
        q = q + SPARQL_EX_VIVO_DESIGN

        if data['ex-tp-ev-question-1'] == 'inhibition':
            q = q + SPARQL_TRANSPORT_INHIBITION
        elif data['ex-tp-ev-question-1'] == 'identification':
            q = q + SPARQL_TRANSPORT_IDENTIFICATION

        if data['ex-tp-ev-question-2'] == 'cacoTwoCellLines':
            q = q + SPARQL_CACO_2_CELL_LINE
        elif data['ex-tp-ev-question-2'] == 'overExpressedCellLines':
            q = q + SPARQL_OVEREXPRESSED_CELL_LINE
        elif data['ex-tp-ev-question-2'] == 'unsure':
            q = q + SPARQL_NOT_OVEREXPRESSED_CELL_LINE + SPARQL_NOT_CACO_2_CELL_LINE


        if data['ex-tp-ev-question-3'] == 'pGlycoprotein':
            q = q + SPARQL_P_GLYCOPROTEIN
        elif data['ex-tp-ev-question-3'] == 'oatpOnebOne':
            q = q + SPARQL_OATP1B1
        elif data['ex-tp-ev-question-3'] == 'oatpOnebThree':
            q = q + SPARQL_OATP1B3
        elif data['ex-tp-ev-question-3'] == 'unsure':
            q = q + SPARQL_NOT_OATP1B1 + SPARQL_NOT_OATP1B3 + SPARQL_NOT_P_GLYCOPROTEIN
            
    # close the query with a request for the matching evidence types 
    q = q + SPARQL_EV_TYPE + '''
}
'''
    print q
    tstore.setQuery(q)
    tstore.setReturnFormat(JSON)
    qr = tstore.query().convert()
    etRslt = ""
    definition = ""
    
    if len(qr["results"]["bindings"]) == 0:
        print "results from sparql query is none "
        etRslt = "No evidence type matching the chosen characteristics"
    else:
        print "results: %s" % qr
        evTypeData = [{"evItem":x["evItem"]["value"] ,"label":x["label"]["value"],"evType":x["evType"]["value"],"definition":x["definition"]["value"]} for x in qr["results"]["bindings"]]
        print "evTypeData: %s" % evTypeData
        curEvItem = ""
        for it in evTypeData:
            if it["evItem"] == curEvItem:
                etRslt += "-->%s" % it["label"]
                definition += "-->%s" % it["definition"]
            else:
                curEvItem = it["evItem"]
                etRslt += "%s" % it["label"]
                definition += "%s" % it["definition"]
        if etRslt == "":
            etRslt = "ERROR: Couldn't infer evidence type"
            
    inferred_evidence_type = (etRslt, definition, inferenceNotes)
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
