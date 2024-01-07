from datetime import datetime
from hired import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    if Recruiter.query.get(int(user_id)):
        return Recruiter.query.get(int(user_id))
    else:
        return User.query.get(int(user_id))


#metadata = db.MetaData()

#Job_User = db.Table('Job_User', metadata,

#                    db.Column('job_id', db.Integer, db.ForeignKey('job.id'), nullable=True),
#                    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=True)

#                    )


class Job_User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        return f"Job_User('{self.job_id}', '{self.user_id}')"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    degree_type = db.Column(db.String(7), nullable=True)
    experience = db.Column(db.Integer, nullable=True)
    major = db.Column(db.String(30), nullable=True)
    skill_1 = db.Column(db.String(30), nullable=True)
    skill_1_level = db.Column(db.Integer, nullable=True)
    dbms = db.Column(db.String(10), nullable=True)

    jobs = db.relationship('Job_User', backref='job', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.degree_type}')"


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, unique=True, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    skill = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(20), nullable=False)
    recruiter_id = db.Column(db.Integer, db.ForeignKey('recruiter.id'), nullable=False)

    users = db.relationship('Job_User', backref='user', lazy=True)

    def __repr__(self):
        return f"Job('{self.company}', '{self.skill}', '{self.location}')"


class Recruiter(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    location = db.Column(db.String(20), nullable=True)
    jobs = db.relationship('Job', backref='company', lazy=True)

    def __repr__(self):
        return f"Recruiter('{self.username}')"
