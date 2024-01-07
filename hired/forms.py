from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from hired.models import User, Recruiter, Job

class RegistrationForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is taken. Please choose a different one.')

class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    degree_type = StringField('Degree', validators=[DataRequired(), Length(min=2, max=7)])
    experience = IntegerField('Experience(In Years)', validators=[DataRequired()])
    major = StringField('Major', validators=[DataRequired(), Length(min=3, max=30)])
    skill_1 = StringField('Skill', validators=[DataRequired(), Length(min=2, max=10)])
    skill_1_level = IntegerField('Skill Level (1-10)', validators=[DataRequired()])
    dbms = StringField('DBMS you are most familiar with', validators=[DataRequired(), Length(min=2, max=10)])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email is taken. Please choose a different one.')

class RecUpdateAccountForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    location = StringField('Base Location', validators=[DataRequired(), Length(min=3, max=20)])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            recruiter = Recruiter.query.filter_by(username=username.data).first()
            if recruiter:
                raise ValidationError('This username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            recruiter = Recruiter.query.filter_by(email=email.data).first()
            if recruiter:
                raise ValidationError('This email is taken. Please choose a different one.')

class CandidateDetailsForm(FlaskForm):
    degree_type = StringField('Degree', validators=[DataRequired(), Length(min=2, max=7)])
    experience = IntegerField('Experience(In Years)', validators=[DataRequired()])
    major = StringField('Major', validators=[DataRequired(), Length(min=3, max=30)])
    skill_1 = StringField('Skill', validators=[DataRequired(), Length(min=2, max=10)])
    skill_1_level = IntegerField('Skill Level (1-10)', validators=[DataRequired()])
    dbms = StringField('DBMS you are most familiar with', validators=[DataRequired(), Length(min=2, max=10)])
    submit = SubmitField('Submit Details')

class CreateJobForm(FlaskForm):
    job_id = IntegerField('Job Id', validators=[DataRequired()])
    skill = StringField('Skill', validators=[DataRequired(), Length(min=2, max=10)])
    location = StringField('Location', validators=[DataRequired(), Length(min=3, max=20)])
    submit = SubmitField('Submit Details')

    def validate_job(self, job_id):
        job = Job.query.filter_by(job_id=job_id.data).first()
        if job:
            raise ValidationError('This job id is taken. Please choose a different one.')

class SelectJobForm(FlaskForm):
    job_id = IntegerField('Enter the Job Id you want to apply for:', validators=[DataRequired()])
    submit = SubmitField('Apply now')
