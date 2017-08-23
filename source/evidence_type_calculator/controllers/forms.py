# -*- coding: utf-8 -*-

def index():

    response.flash = T("test")
    return dict(message=T('evidence type form!'))


def evidenceTypeQuestions():

    print '[INFO] controller evidenceTypeQuestions...'
    print request.vars
    print request.vars.evidencetype

    for k in request.vars:
        print k, request.vars[k]
    # db.evidence_type.insert(id=2, document_id=2, participant='user1', method='DDI clinical trial')
    # evidence type question form submit
    
    
    print db.executesql('SELECT * FROM evidence_type;')
    
    return dict(message=T('Evidence type questions submit!'))

