# import os, sys

# # db = DAL('sqlite://storage.sqlite')

# # evidence type form
# db.define_table('evidence_type_form', Field('is_started', type='boolean'), Field('is_finished', type='boolean'))

# db.define_table('evidence_type_question', Field('evidence_type_form_id', db.evidence_type_form), Field('question', type='string'), Field('answer', type='string'))

# # following form
# db.define_table('following_form', Field('is_started', type='boolean'), Field('is_finished', type='boolean'))

# db.define_table('following_question', Field('following_form_id', db.following_form), Field('question', type='string'), Field('answer', type='string'))

# # sub method type
# db.define_table('sub_method', Field('sub_method_name', type='string'), Field('sub_method_level', type='integer'))

# # evidence type
# db.define_table('evidence_type', Field('document_id', type='string'), Field('participant', type='string'), Field('mp_method', type='string'), Field('evidence_type_form_id', db.evidence_type_form), Field('following_form_id', db.following_form), Field('sub_method_id', db.sub_method), Field('inferred_evidence_type', type='string'), Field('is_started', type='boolean'), Field('is_finished', type='boolean'), Field('is_agree_with_inference', type='boolean'), Field('disagree_comment', type='string'))

# # sample data
# db.evidence_type.insert(document_id='PMC123456', participant='Yifan', mp_method="DDI clinical trial")
# db.evidence_type.insert(document_id='PMC234567', participant='Yifan', mp_method="DDI clinical trial")
