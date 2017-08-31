import os, sys

## maps for question code and full question content
qsMap = {"ct-gr": "Group Randomization?", "ct-pgd": "Parallel Group Design?", "ct-pk": "Study Focused on Pharmacokinetic Processes?", "ct-ph": "Phenotyping?", "ct-gt": "Genotyping?", "cr-ae": "Reporting an adverse event?", "cr-pr": "Publically reported?", "cr-ep": "Icl an evaluation protocol?", "exp-m-st": "Subtype?", "exp-m-at": "Assay Type?", "exp-m-mi": "Metabolic Inhibitor?", "exp-t-st": "Subtype?", "exp-t-at": "Assay Type?", "exp-t-tp": "Transporter Protein?"}

db = DAL('sqlite://storage.sqlite', fake_migrate=True)

# evidence type form
db.define_table('evidence_type_form', Field('is_started', type='boolean'), Field('is_finished', type='boolean'))

db.define_table('evidence_type_question', Field('evidence_type_form_id', db.evidence_type_form), Field('question', type='string'), Field('answer', type='string'))

# icl form
db.define_table('icl_form', Field('is_started', type='boolean'), Field('is_finished', type='boolean'))

db.define_table('icl_question', Field('icl_form_id', db.icl_form), Field('question', type='string'), Field('answer', type='string'))

# sub method type
db.define_table('sub_method', Field('sub_method_name', type='string'), Field('sub_method_level', type='integer'))

# evidence type
db.define_table('evidence_type', Field('task_id', type='string'), Field('participant', type='string'), Field('mp_method', type='string'), Field('evidence_type_form_id', db.evidence_type_form), Field('icl_form_id', db.icl_form), Field('sub_method_id', db.sub_method), Field('inferred_evidence_type', type='string'), Field('entered_evidence_type', type='string'), Field('is_started', type='boolean'), Field('is_finished', type='boolean'), Field('is_agree_with_inference', type='boolean'), Field('disagree_comment', type='string'))

# participant task
db.define_table('participant_task', Field('participant', type='string'), Field('code', type='string'), Field('task_id', type='integer'), Field('assist', type='boolean'))

## clean all tables
db.evidence_type.truncate()
db.evidence_type_form.truncate()
db.evidence_type_question.truncate()
db.participant_task.truncate()

# assign tasks to participants, based on config in uploads/participant_task.csv
pathfilename=os.path.join(request.folder,'config/', 'participant_task.csv')
db.participant_task.import_from_csv_file(open(pathfilename), delimiter=",")



