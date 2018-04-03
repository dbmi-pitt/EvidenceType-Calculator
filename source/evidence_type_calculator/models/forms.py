print "[INFO] forms model init..."

# map for evidence type question ui-code and full question content
# TODO: all of this should be generated from a SPARQL query of the
# DIKB IC annotation properties in the DIDEO ontology. This will save
# maintainance time and utilize the hierarchical structure of the
# ontology
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

                    
                    "IC1": "Are pharmacokinetic measurement sampling times sufficent to characterize AUC_{0 to INF} (for single-dose studies), AUC_{0 to TAU} (for multi-dose studies), maximum concentration (Cmax) and the minimum concentration (Cmin) of the victim (substrate) drug administered alone and under conditions of the anticipated interaction?",
                    "IC2":"Are the pharmacokinetic results reported as the geometric mean ration of the observed pharmacokinetic exposure measures with and without the perpretrator drug, including 90% confidence intervals and measures of the observed variability of the interaction?",
                    "IC3":"Do the pharmacokinetic measurements include samples of all moieties needed to interpret study results, including metabolites if that information provides information about the interaction effect and/or safety?",
                    "IC4":"Does the study properly exclude and/or account for the use of prescription or OTC medications, dietary/nutritional supplements, tobacco, alcohol, foods, and fruit juices that may affect the expression or function of enzymes and transporters?",
                    "IC5":"If either of the drugs used in the study require different food conditions for optimal asborption, is the timing of drug administration designed to maximize the potential to either detect an interaction or reflect clinically relevant conditions?",
                    "IC6":"If the perpretator drug is both an inhibitor and inducer of CYP enzymes, does the study delay administration of the victim drug?",
                    "IC7":"If the perpretrator dosing regimen is single dose, were plasma samples collected and analyzed to ensure that both clinically relevant concentrations and maximal inhibition was achieved?",
                    "IC8":"If the study is a single-dose study, are the pharmacokinetic measurement sampling times planned so that the mean difference between the AUC_{0 to t} and the AUC_{0 to INF} is less than 20%?",
                    "IC9":"If the study is testing whether a drug is a perpretrator of pharmacokinetic drug-drug interactions, does the study use an index CYP substrate as defined in Table2-1 (https://goo.gl/NwSkxX) or an index transport enzyme substrate as defined in Table5-1 (https://goo.gl/2jHM3w) of FDA guidance ucm093664?",
                    "IC10":"If the study is testing whether a drug is a victim of pharmacokinetic drug-drug interactions, does the study use an CYP index perpretrator as defined in Table2-2 (https://goo.gl/hWLmqJ) or a transport enzyme index perpretator as defined in Table5-2 (https://goo.gl/8LrGvL) of FDA guidance ucm093664?",
                    "IC11":"If the study is uses a victim (drug) drug that is metabolized by more than one CYP metabolizing enzyme, is the perpretator (precipitant) drug a selective inhibitor or inducer of the victim drug's primary CYP metabolizing enzyme (i.e., the CYP enzyme that is involved in more that 50% of the drug's metabolic clearance)?",
                    "IC12":"If the the perpretrator is a time-dependent pharmacokinetic inhibitor or potential inducer, is a multi-dose regimen used in the study?",
                    "IC13":"If the victim (substrate) drug is known to display dose- or time-dependent non-linear pharmacokinetics, were multiple doses of the victim given to participants?",
                    "IC14":"If the victim drug has linear pharmacokinetics, is the dose used in the study in the linear therapeutic range?",
                    "IC15":"If the victim drug has non-linear pharmacokinetics, is the dose used in the study the one that is most likely to demonstrate a drug-drug interaction after taking safety into consideration?",
                    "IC16":"Is the dose of the perpretator drug sufficient to identify a drug-drug interaction?",
                    "IC17":"Is the number of study participants sufficient to provide a reliable estimate of the magnitude and variability of the interaction?",
                    "IC18":"Is the route of administration of the drug that is the focus of the drug-drug interaction study the one that is generally planned for routine clinical use?",
                    "IC19":"If the perpretator is an inducer, does the dosing regimen ensure maximal induction of the relevant pharmacokinetic pathway?",
                    "IC20":"If the study design is a parallel, two-arm, study, does the sample size properly account for intersubject variability?",
                    "IC21":"If the study design is a parallel, two-arm, study, does the sample size properly account for intersubject variability?",
                    "IC22":"If the study design is a two-way crossover design, does the washout period properly account for 1) the known pharmacokinetics of the victim (substrate) and perpetrator (precipitant) drugs, and 2) the anticipated impact of a drug-drug interaction on the victim's half-life?",


                    
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
global_ct_ic_qs_codes = ["IC1","IC2","IC3","IC4","IC5","IC6","IC7","IC8","IC9","IC10","IC11","IC12","IC13","IC14","IC15","IC16","IC17","IC18","IC19","IC20","IC21","IC22"]
global_ex_mt_ic_qs_codes = ["ex-mt-ic-question-1", "ex-mt-ic-question-2", "ex-mt-ic-question-3", "ex-mt-ic-question-4"]
global_ex_tp_ic_qs_codes = ["ex-tp-ic-question-1", "ex-tp-ic-question-2", "ex-tp-ic-question-3", "ex-tp-ic-question-4"]
