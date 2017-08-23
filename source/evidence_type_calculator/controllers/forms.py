# -*- coding: utf-8 -*-

def index():

    response.flash = T("test")
    return dict(message=T('evidence type form!'))


def clinicalTrialForm():

    print '[INFO] controller forms: clinicalTrialForm()...'
    print request.vars
    # db.evidence_type.insert(id=2, document_id=2, participant='user1', method='DDI clinical trial')
    print db.executesql('SELECT * FROM evidence_type;')
    
    return dict(message=T('clinical trial submit!'))


def caseReportForm():

    print '[INFO] controller forms: caseReportForm()...'
    print request.vars

    # db = DAL('sqlite://storage.sqlite', pool_size=0)
    return dict(message=T('clinical trial submit!'))
