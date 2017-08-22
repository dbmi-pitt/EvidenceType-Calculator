# -*- coding: utf-8 -*-

def index():

    response.flash = T("test")
    return dict(message=T('evidence type form!'))


def clinicalTrialForm():

    print '[INFO] controller forms: clinicalTrialForm()...'
    print request.vars
    return dict(message=T('clinical trial submit!'))


def caseReportForm():

    print '[INFO] controller forms: caseReportForm()...'
    print request.vars
    return dict(message=T('clinical trial submit!'))
