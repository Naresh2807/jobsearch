1. Recommended IDE - PyCharm (Possible to run run.py and importcsv.py at the same time.)
2. Debug mode is ON. To switch to regular mode, remove debug=True from run.py (Not recommended until project is to be submitted)
3. To start the application, run run.py. Click on the output link (http://localhost:5000/) to start the website. This provides candidate side access.
4. For recruiter side access, use subdomain recruit. Example : http://recruiter.localhost:5000/
5. importcsv.py can be run to add new jobs, candidates, recruiters from csv files to the database.
6. To view the database tables
 a. http://localhost:5000/user_list
 b. http://localhost:5000/recruiter_list
 c. http://localhost:5000/job_list
7. To delete all tables, open command prompt in the folder, type “python” to open python console (or directly open python console from the bottom bar in PyCharm) and type the following -
 a. from hired import db (2 red lines will appear but nothing to worry about)
 b. from hired.models import User, Recruiter, Job, Job_User
 c. db.drop_all() { Now the links to database tables gives error }
 d. db.create_all() {Now the links to database tables show zero values}
8. To load values from csv again, run importcsv.py. 
9. For new values added to csv, run importcsv.py again to add to the database. Old values remain untouched. Updation functionality via csv but would have to delete and load again.
