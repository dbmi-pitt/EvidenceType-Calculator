print "[INFO] forms model init..."

# map for evidence type question ui-code and full question content
global_ev_qs_map = {"ct-ev-question-1": "Group Randomization?",
                    "ct-ev-question-2": "Parallel Group Design?",
                    "ct-ev-question-3": "Study assesses individual drug pharmacokinetics?",
                    "ct-ev-question-4": "Phenotyping?",
                    "ct-ev-question-5": "Genotyping?",
                    
                    "cr-ev-question-1": "Reporting an adverse event?",
                    "cr-ev-question-2": "Publicly (spontaneously) reported?",
                    "cr-ev-question-4": "Involves a suspected drug-drug interaction?",
                    "cr-ev-question-3": "Was an evaluation of adverse event causality conducted?",
                    
                    "ex-ev-mt-question-1": "Mechanism?",
                    "ex-ev-mt-question-4": "Focused on a CYP450 enzyme?",                    
                    "ex-ev-mt-question-2": "Assay type?",
                    "ex-ev-mt-question-3": "Inhibitor type?",
                    
                    "ex-tp-ev-question-1": "Mechanism?",
                    "ex-tp-ev-question-2": "Assay Type?",
                    "ex-tp-ev-question-3": "Transporter Protein?"}

# map for inclusion criteria question ui-code and full question content
global_ic_qs_map = {"cr-ic-question-1": "Previous Credible Reports in Humans?",
                    "cr-ic-question-2": "Interaction Consistent with Known Interactive Qualities of the Precipitant Drug?",
                    "cr-ic-question-3": "Interaction Consistent with Known Interactive Qualities of the Object Drug?",
                    "cr-ic-question-4": "Interaction Consistent with Known Reasonable Time Course of the Interaction (onset and/or offest)?",
                    "cr-ic-question-5": "Did the interaction remit upon de-challenge of the precipitant drug with no change in oject drug? (If no de-challenge, use unknown and skip to question 6)?",
                    "cr-ic-question-6": "Did the interaction reappear when precipitant drug was readministered with continued used of object drug?",
                    "cr-ic-question-7": "Reasonable alernative causes?",
                    "cr-ic-question-8": "Was the object drug detected in the blood or other fluids in concentrations consistent with the interaction?",
                    "cr-ic-question-9": "Was the drug interaction confirmed by objective evidence consistent with the affects on the object drug (other than from question 8)?",
                    "cr-ic-question-10": "Was the interaction greater when the precipitant dose was increased or less when the precipitant dose was decreased?",

                    
                    "ct-ic-question-1": "Was there a polymorphic assertion linked as an assumption for the intended use of the evidence item?",
                    "ct-ic-question-2": "Was the specific genotype of the enzyme  noted in the description of evidence?",
                    "ct-ic-question-3": "If the substrate is being evaluated to support or refute that drug is a substrate of P-Glycoprotein, did the study compare wild type to variants in ABCB1 including 3435C$>$T, 2677G$>$T and 1236C$>$T?",
                    "ct-ic-question-4": "If the substrate is being evaluated to support or refute that drug is a substrate of OATP1B1, did the study compare wild type to variants in SLCO1B1?",
                    "ct-ic-question-5": "If the substrate is being evaluated to support of refute that a drug is a substrate of OATP1B3, did the study compare wild type to variants in SLCO1B3?",

                    
                    "ex-mt-ic-question-1": "Enzyme Source:",
                    "ex-mt-ic-question-2": "NADPH Regenerating System:",
                    "ex-mt-ic-question-3": "Antibody Inhibitors:",
                    "ex-mt-ic-question-4": "In Vitro Selective Inhibitors:",

                    
                    "ex-tp-ic-question-1": "Animal Study:",
                    "ex-tp-ic-question-2": "In Vitro Inhibitor:",
                    "ex-tp-ic-question-3": "Cell Line for P-Glycoprotein:",
                    "ex-tp-ic-question-4": "Appropriate Controls:"}

# list of evidence type question ui-element codes based on different high level evidence type
global_cr_ev_qs_codes = ["cr-ev-question-1", "cr-ev-question-2", "cr-ev-question-4", "cr-ev-question-3" ]
global_ct_ev_qs_codes = ["ct-ev-question-1", "ct-ev-question-2", "ct-ev-question-3", "ct-ev-question-4", "ct-ev-question-5"]
global_ex_mt_ev_qs_codes = ["ex-ev-mt-question-1", "ex-ev-mt-question-2", "ex-ev-mt-question-4", "ex-ev-mt-question-3"]
global_ex_tp_ev_qs_codes = ["ex-ev-tp-question-1", "ex-ev-tp-question-2", "ex-ev-tp-question-3"]

# list of inclusion criteria question ui-element codes based on different high level evidence type 
global_cr_ic_qs_codes = ["cr-ic-question-1", "cr-ic-question-2", "cr-ic-question-3", "cr-ic-question-4", "cr-ic-question-5", "cr-ic-question-6", "cr-ic-question-7", "cr-ic-question-8", "cr-ic-question-9", "cr-ic-question-10"]
global_ct_ic_qs_codes = ["ct-ic-question-1", "ct-ic-question-2", "ct-ic-question-3", "ct-ic-question-4", "ct-ic-question-5"]
global_ex_mt_ic_qs_codes = ["ex-mt-ic-question-1", "ex-mt-ic-question-2", "ex-mt-ic-question-3", "ex-mt-ic-question-4"]
global_ex_tp_ic_qs_codes = ["ex-tp-ic-question-1", "ex-tp-ic-question-2", "ex-tp-ic-question-3", "ex-tp-ic-question-4"]
