from flask import render_template, url_for, flash, redirect, request
from hired import app, db, bcrypt
from hired.forms import RegistrationForm, LoginForm, UpdateAccountForm, RecUpdateAccountForm, CreateJobForm, \
    SelectJobForm
from hired.models import User, Recruiter, Job, Job_User
from flask_login import login_user, current_user, logout_user, login_required
import urllib

# from hired.import_csv import recruiter_list

posts = [
    {
        'title': 'Join Us @ Amazon',
        'author': 'Amazon',
        'date_posted': '22/01/20',
        'content': 'Looking for fresh talent.  \n Join our family. \n Everyone has a place here. \n We make the world a better place.'
    },
    {
        'title': 'Looking to start fresh',
        'author': 'Enakshi Jamwal',
        'date_posted': '22/01/20',
        'content': 'Recently graduated from MPSTME. \n Specialise in UX Design. \n Excited to start working. \n Ready to join as soon as quarantine is over.'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About Us')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit()==True:
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=form.remember.data)
        flash('Your account has been created. You can now enter your information.', 'success')
        return redirect(url_for('account'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            # subdomain = request.url.hostname.split('.')[0]
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.degree_type = form.degree_type.data
        current_user.experience = form.experience.data
        current_user.major = form.major.data
        current_user.skill_1 = form.skill_1.data
        current_user.skill_1_level = form.skill_1_level.data
        current_user.dbms = form.dbms.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.degree_type.data = current_user.degree_type
        form.experience.data = current_user.experience
        form.major.data = current_user.major
        form.skill_1.data = current_user.skill_1
        form.skill_1_level.data = current_user.skill_1_level
        form.dbms.data = current_user.dbms
    # image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    image_file = url_for('static', filename='default.jpg')
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route('/user_list')
def user_list():
    users = User.query.all()
    return render_template('user_list.html', title='Candidates List', users=users)


@app.route('/job_list')
def job_list():
    jobs = Job.query.all()
    return render_template('job_list.html', title='Jobs List', jobs=jobs)


@app.route('/recruiter_list')
def recruiter_list():
    recruiters = Recruiter.query.all()
    return render_template('recruiter_list.html', title='Recruiters List', recruiters=recruiters)


@app.route('/', subdomain='recruit')
@app.route('/home', subdomain='recruit')
def home_rec():
    return render_template('home_rec.html', posts=posts)


@app.route('/test', subdomain='recruit')
def test():
    return render_template('test.html', title='Test')


@app.route('/recruiter_list', subdomain='recruit')
def recruiter_list_rec():
    recruiters = Recruiter.query.all()
    return render_template('recruiter_list.html', title='Recruiters List', recruiters=recruiters)


@app.route('/register', subdomain='recruit', methods=['GET', 'POST'])
def register_rec():
    if current_user.is_authenticated:
        return redirect(url_for('home_rec'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        recruiter = Recruiter(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(recruiter)
        db.session.commit()
        login_user(recruiter, remember=form.remember.data)
        flash('Your account has been created. You can now enter your information.', 'success')
        return redirect(url_for('account_rec'))
    return render_template('register_rec.html', title='Register', form=form)


@app.route('/login', subdomain='recruit', methods=['GET', 'POST'])
def login_rec():
    if current_user.is_authenticated:
        return redirect(url_for('home_rec'))
    form = LoginForm()
    if form.validate_on_submit():
        recruiter = Recruiter.query.filter_by(email=form.email.data).first()
        if recruiter and bcrypt.check_password_hash(recruiter.password, form.password.data):
            login_user(recruiter, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home_rec'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('login_rec.html', title='Login', form=form)


@app.route('/logout', subdomain='recruit')
def logout_rec():
    logout_user()
    return redirect(url_for('home_rec'))


@app.route('/account', methods=['GET', 'POST'], subdomain='recruit')
@login_required
def account_rec():
    form = RecUpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.location = form.location.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account_rec'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.location.data = current_user.location
    # image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    image_file = url_for('static', filename='default.jpg')
    return render_template('account_rec.html', title='Account', image_file=image_file, form=form)


@app.route('/view_jobs', methods=['GET'], subdomain='recruit')
@login_required
def view_jobs():
    jobs = Job.query.filter_by(company=current_user).all()
    return render_template('job_list.html', title='Jobs List', jobs=jobs)


@app.route('/create_jobs', methods=['GET', 'POST'], subdomain='recruit')
@login_required
def create_jobs():
    form = CreateJobForm()
    if form.validate_on_submit():
        job = Job(job_id=form.job_id.data, company=current_user, skill=form.skill.data, location=form.location.data)
        db.session.add(job)
        db.session.commit()
        flash('Your job has been created!', 'success')
        return redirect(url_for('view_jobs'))
    image_file = url_for('static', filename='default.jpg')
    return render_template('create_jobs.html', title='Create Jobs', image_file=image_file, form=form)


@app.route('/select_jobs', methods=['GET', 'POST'])
@login_required
def select_jobs():
    form = SelectJobForm()
    print(form.job_id.data)
    jobs = Job.query.all()
    if form.validate_on_submit():
        job = Job.query.filter_by(job_id=form.job_id.data).first()
        job_user = Job_User()
        job_user.job_id = job.job_id
        job_user.user_id = current_user.get_id()
        # job_user = Job_User(job=job, user=current_user)
        db.session.add(job_user)
        db.session.commit()
        flash('Your job has been selected!', 'success')
        return redirect(url_for('view_jobs_can'))
    return render_template('select_jobs.html', title='Select Jobs', form=form, jobs=jobs)


@app.route('/view_jobs', methods=['GET', 'POST'])
@login_required
def view_jobs_can():
    job_users = Job_User.query.filter_by(user_id=current_user.get_id()).all()
    lis = []
    jobs = []
    for ju in job_users:
        lis.append(ju.job_id)
    print(lis)
    for x in lis:
        jobs.append(Job.query.filter_by(job_id=x).first())
    print(jobs)
    return render_template('view_jobs.html', title='Jobs List', jobs=jobs)

@app.route('/view_candidates', methods=['GET', 'POST'], subdomain='recruit')
@login_required
def view_cans():
    jobs = Job.query.filter_by(company=current_user).all()
    lis = []
    jus = []
    jlist = []
    for j in jobs:
        lis.append(j.job_id)
    for x in lis:
        jus.append(Job_User.query.filter_by(job_id=x).first())
    lis = []
    cans = []
    for ju in jus:
        if ju is not None:
            lis.append(ju.user_id)
            jlist.append(ju.job_id)
    print(jlist)
    for x in lis:
        cans.append(User.query.filter_by(id=x).first())
    return render_template('view_cans.html', title='Candidates List', users=cans, job_ids=jlist, i=0)
