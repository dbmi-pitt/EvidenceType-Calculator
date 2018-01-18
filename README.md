-----------
EvidenceType-Calculator
-----------

This project purpose for supporing identify most specific evidence type, serving form of evidence type related questions for Drug drug interaction including Clinical trial, Phenotype clinical study, Experiments, Case Report, etc. An example of how the system works can be seen here:

https://docs.google.com/presentation/d/1g5FDLzVJnb0jIr9wQ8YlGIEBag4t6ioupZyd24hi8TE

-----------
Deployment
-----------

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