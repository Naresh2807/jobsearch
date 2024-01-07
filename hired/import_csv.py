import pandas as pd
from hired.models import User, Recruiter, Job, Job_User
from hired import db, bcrypt

candidate_list = pd.read_csv("C:\\Users\\DELL 3468\\Desktop\\Stuff\\4th Year Now\\FY Project\\Project\\FlaskHired\\hired\\applicant.csv")
candidate_list = candidate_list.values.tolist()

job_list = pd.read_csv("C:\\Users\\DELL 3468\\Desktop\\Stuff\\4th Year Now\\FY Project\\Project\\FlaskHired\\hired\\jobposting.csv")
job_list = job_list.values.tolist()

recruiter_list = pd.read_csv("C:\\Users\\DELL 3468\\Desktop\\Stuff\\4th Year Now\\FY Project\\Project\\FlaskHired\\hired\\recruiter.csv")
recruiter_list = recruiter_list.values.tolist()

default_password = bcrypt.generate_password_hash('pass1234').decode('utf-8')

ccount = 0
jcount = 0
rcount = 0

for row in candidate_list:
    if User.query.filter_by(username=row[1]).first():
       ccount += 1
    else:
        user = User(username=row[1], email=row[2], password=default_password, image_file=row[3], degree_type=row[4], experience=row[5], major=row[6], skill_1=row[7], skill_1_level=row[8], dbms=row[9])
        db.session.add(user)

print(ccount, 'Candidate(s) already exist')

db.session.commit()

for row in recruiter_list:
    if Recruiter.query.filter_by(username=row[0]).first():
        rcount += 1
    else:
        recruiter = Recruiter(username=row[0], email=row[1], password=default_password, image_file=row[2], location=row[3])
        db.session.add(recruiter)

print(rcount, 'Recruiter(s) already exist')

db.session.commit()


for row in job_list:
    if Job.query.filter_by(job_id=row[1]).first():
        jcount += 1
    else:
        rec = Recruiter.query.filter_by(username=row[2]).first()
        job = Job(job_id=row[1], company=rec, skill=row[3], location=row[4])
        db.session.add(job)

print(jcount, 'Job(s) already exist')

db.session.commit()
