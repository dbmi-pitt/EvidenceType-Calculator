-----------
EvidenceType-Calculator
-----------

This project purpose for supporing identify most specific evidence type, serving form of evidence type related questions for Drug drug interaction including Clinical trial, Phenotype clinical study, Experiments, Case Report, etc. An example of how the system works can be seen here:

https://docs.google.com/presentation/d/1g5FDLzVJnb0jIr9wQ8YlGIEBag4t6ioupZyd24hi8TE

-----------
Deployment
-----------
Pre-requisite:
This application submits SPARQL 1.1 queries to an endpoint (currently http://localhost:8890/sparql unless customized). The endpoint requires the following graphs to be loaded:

- individuals.owl from commit 9881834 of https://github.com/DIDEO/DIDEO/tree/john/evidence-type-merge loaded as http://purl.obolibrary.org/obo/dideo.owl#. This version of DIDEO has the inclusion criteria as object properties.

- dikb-etypes-04042018.xml from 9881834 of https://github.com/DIDEO/DIDEO/tree/john/evidence-type-merge loaded as http://www.semanticweb.org/rdb20/ontologies/2018/1/dikb-etypes-04042018#. This data file holds the inferred instance types.



Web2py framework
Download:
http://www.web2py.com/init/default/download

Tutorial:
http://www.tutorialspoint.com/web2py/

Development:
Make symbolic link to web2py applications directory
Example on Linux:
ln -s /path/to/EvidenceType-Calculator /path/to/web2py/applications/

Save modifications in git repository and refresh web2py index page will see your changes
Example:
http://127.0.0.1:8000/evidence_type_calculator/default/index

---------------
Initiate study
---------------

Requires csv file for assign tasks to users.
columns: userId, evidenceId, assistWithInference