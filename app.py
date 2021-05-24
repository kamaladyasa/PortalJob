from flask_migrate import Migrate
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import base64
import uuid
from flask_bcrypt import Bcrypt, check_password_hash
import re
from datetime import datetime
from sqlalchemy import or_, and_, func
from sqlalchemy.sql import label
from flask_cors import CORS, cross_origin

cors_config = {
    "origins": ["http://127.0.0.1:5001"],
    "methods": ["GET", "POST", "PUT", "DELETE"]
}

app = Flask(__name__)
CORS(app, resources={
    r"/*": cors_config
})

db = SQLAlchemy()
bcrypt = Bcrypt(app)

app.config['SECRET_KEY']='secret'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:P@ssw0rd@localhost:5432/portaljob'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

migrate = Migrate(app, db)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40))
    date_of_birth = db.Column(db.DateTime, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_edu = db.relationship('EducationDetail', backref = 'uedu', lazy = 'dynamic')
    user_exp = db.relationship('ExperienceDetail', backref = 'uexp', lazy = 'dynamic')
    jp_activity = db.relationship('JobPostActivity', backref = 'jpactivity', lazy = 'dynamic')

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    company_name = db.Column(db.String(70), nullable=False)
    website = db.Column(db.String(40))
    contact_number = db.Column(db.String(20), nullable=False)
    profile_description = db.Column(db.String(1000))
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(40), nullable=False)
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    jp_company = db.relationship('JobPost', backref = 'jpcom', lazy = 'dynamic')

class EducationDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    last_education = db.Column(db.String(30), nullable=False)
    major = db.Column(db.String(50), nullable=False)
    univ_name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    complete_date = db.Column(db.DateTime)
    gpa = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class ExperienceDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    job_title = db.Column(db.String(50))
    company_name = db.Column(db.String(100))
    job_location_city = db.Column(db.String(50))
    description_job = db.Column(db.String(2000))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class JobPost(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String(50), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    job_description = db.Column(db.String(1000))
    location_city = db.Column(db.String(50), nullable=False)
    specialization = db.Column(db.String(70), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    jp_activity = db.relationship('JobPostActivity', backref = 'jpact', lazy = 'dynamic')

class JobPostActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_post_id = db.Column(db.Integer, db.ForeignKey('job_post.id'), nullable=False)
    apply_date = db.Column(db.DateTime, nullable=False, default=datetime.now)

def login():
    res = request.headers.get("Authorization")
    # if not res:
    #     return {'error': 'Login Error'}
    a = res.split()
    u = base64.b64decode(a[-1]).decode('utf-8')
    b = u.split(":")
    return b

def encrypt(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

@app.route('/users/')
def get_users():
    return jsonify([
        {
        'id': u.id, 'password': u.password, 'email': u.email, 'first_name': u.first_name,
        'last_name': u.last_name, 'date_of_birth': u.date_of_birth, 'gender': u.gender,
        'contact_number': u.contact_number, 'registration_date': u.registration_date
        } for u in Users.query.all()
    ])

@app.route('/users/<id>/')
def get_user(id):
    print(id)
    user = Users.query.filter_by(id=id).first_or_404()
    return {
        'id': user.id, 'password': user.password, 'email': user.email, 'first_name': user.first_name,
        'last_name': user.last_name, 'date_of_birth': user.date_of_birth, 'gender': user.gender,
        'contact_number': user.contact_number, 'registration_date': user.registration_date
    }

###### REGISTER USER ######
@app.route('/users/', methods=['POST'])
def create_user():
    data = request.get_json()
    if not 'email' or not 'password' or not 'first_name' or not 'last_name' or not 'date_of_birth' or not 'gender' or not 'contact_number' in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Input not valid'
        }), 400
    if 'email' not in data: return {'message': 'Email not given'}, 400
    pattern = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if not (re.search(pattern, data['email'])):
        return jsonify({
            'error': 'Bad Request',
            'message': 'Not a valid email'
        }), 400
    if 'password' not in data: return {'message': 'Password not given'}, 400
    count=0
    while True:
        if len(data['password']) < 6:
            count = -1
            break
        elif not re.search("[a-z]", data['password']):
            count = -1
            break
        elif not re.search("[0-9]", data['password']):
            count = -1
            break
        elif re.search("\s", data['password']):
            count = -1
            break
        else:
            count = 0
            break
    if count == -1:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Password not valid must be contain alphabet and number minimum of 6 letters'
        }), 400
    if 'first_name' not in data: return {'message': 'First name not given'}, 400
    if 'last_name' not in data: return {'message': 'Last name not given'}, 400
    if 'date_of_birth' not in data: return {'message': 'Date of birth not given'}, 400
    if 'gender' not in data: return {'message': 'Gender not given'}, 400
    if 'contact_number' not in data: return {'message': 'Contact number not given'}, 400
    pw_hash = encrypt(data['password'])
    u = Users(
        email = data['email'],
        password = pw_hash,
        first_name = data['first_name'],
        last_name = data['last_name'],
        date_of_birth = data['date_of_birth'],
        gender = data['gender'],
        contact_number = data['contact_number']
    )
    db.session.add(u)
    db.session.commit()
    return {
        'id': u.id, 'password': u.password, 'email': u.email, 'first_name': u.first_name,
        'last_name': u.last_name, 'date_of_birth': u.date_of_birth, 'gender': u.gender,
        'contact_number': u.contact_number, 'registration_date': u.registration_date
    }, 201

###### UPDATE USER ######
@app.route('/users/', methods=['PUT'])
def update_user():
    email, password = login()
    us = Users.query.filter_by(email=email).first()
    if us is None or not bcrypt.check_password_hash(us.password, password):
        return {'error': 'Login Error'}, 401

    data = request.get_json()
    user = Users.query.filter_by(id=us.id).first_or_404()
    
    if 'email' in data:
        pattern = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        if not (re.search(pattern, data['email'])):
            return jsonify({
                'error': 'Bad Request',
                'message': 'Not a valid email'
            }), 400
        user.email = data['email']
    if 'password' in data:
        count=0
        while True:
            if len(data['password']) < 6:
                count = -1
                break
            elif not re.search("[a-z]", data['password']):
                count = -1
                break
            elif not re.search("[0-9]", data['password']):
                count = -1
                break
            elif re.search("\s", data['password']):
                count = -1
                break
            else:
                count = 0
                break
        if count == -1:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Password not valid must be contain alphabet and number minimum of 6 letters'
            }), 400
        pw_hash = encrypt(data['password'])
        user.password = pw_hash
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'date_of_birth' in data:
        user.date_of_birth = data['date_of_birth']
    if 'gender' in data:
        user.gender = data['gender']
    if 'contact_number' in data:
        user.contact_number = data['contact_number']
    db.session.commit()
    return jsonify({
        'id': user.id, 'password': user.password, 'email': user.email, 'first_name': user.first_name,
        'last_name': user.last_name, 'date_of_birth': user.date_of_birth, 'gender': user.gender,
        'contact_number': user.contact_number, 'registration_date': user.registration_date
    })

@app.route('/companies/')
def get_companies():
    return jsonify([
        {
        'id': c.id, 'password': c.password, 'email': c.email, 'company_name': c.company_name,
        'website': c.website, 'profile_description': c.profile_description,
        'contact_number': c.contact_number, 'address': c.address, 'city': c.city, 'registration_date': c.registration_date
        } for c in Company.query.all()
    ])

###### SEARCH USER BY NAME FOR COMPANY ######
@app.route('/companies/search-users/<id>')
def get_user_companies(id):
    email, password = login()
    c = Company.query.filter_by(email=email).first()
    if c is None or not bcrypt.check_password_hash(c.password, password):
        return {'error': 'Login Error'}, 401
    
    print(id)
    return jsonify([
        {
        'id': u.id, 'email': u.email, 'first_name': u.first_name,
        'last_name': u.last_name, 'date_of_birth': u.date_of_birth, 'gender': u.gender,
        'contact_number': u.contact_number
        } for u in db.session.query(Users).filter(or_(Users.first_name.match(id), Users.last_name.match(id)))
    ])

###### REGISTER COMPANY ######
@app.route('/companies/', methods=['POST'])
def create_company():
    data = request.get_json()
    if not 'email' or not 'password' or not 'company_name' or not 'website' or not 'profile_description' or not 'address' or not 'city' or not 'contact_number' in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Input not valid'
        }), 400
    pattern = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if 'email' not in data: return {'message': 'Email not given'}, 400
    if not (re.search(pattern, data['email'])):
        return jsonify({
            'error': 'Bad Request',
            'message': 'Not a valid email'
        }), 400
    if 'password' not in data: return {'message': 'Password not given'}, 400
    count=0
    while True:
        if len(data['password']) < 6:
            count = -1
            break
        elif not re.search("[a-z]", data['password']):
            count = -1
            break
        elif not re.search("[0-9]", data['password']):
            count = -1
            break
        elif re.search("\s", data['password']):
            count = -1
            break
        else:
            count = 0
            break
    if count == -1:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Password not valid must be contain alphabet and number minimum of 6 letters'
        }), 400
    if 'company_name' not in data: return {'message': 'Company name not given'}, 400
    if 'address' not in data: return {'message': 'Company address not given'}, 400
    if 'city' not in data: return {'message': 'Company city not given'}, 400
    if 'contact_number' not in data: return {'message': 'Company contact number not given'}, 400
    pw_hash = encrypt(data['password'])
    c = Company(
        email = data['email'],
        password = pw_hash,
        company_name = data['company_name'],
        website = data['website'],
        profile_description = data['profile_description'],
        address = data['address'],
        city = data['city'],
        contact_number = data['contact_number']
    )
    db.session.add(c)
    db.session.commit()
    return {
        'id': c.id, 'password': c.password, 'email': c.email, 'company_name': c.company_name,
        'website': c.website, 'profile_description': c.profile_description,
        'contact_number': c.contact_number, 'address': c.address, 'city': c.city, 'registration_date': c.registration_date
    }, 201

###### UPDATE COMPANY ######
@app.route('/companies/', methods=['PUT'])
def update_company():
    email, password = login()
    c = Company.query.filter_by(email=email).first_or_404()
    if c is None and not bcrypt.check_password_hash(c.password, password):
        return {'error': 'Login Error'}, 401

    data = request.get_json()
    company = Company.query.filter_by(id=c.id).first_or_404()
    
    if 'email' in data:
        pattern = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        if not (re.search(pattern, data['email'])):
            return jsonify({
                'error': 'Bad Request',
                'message': 'Not a valid email'
            }), 400
        company.email = data['email']
    if 'password' in data:
        count=0
        while True:
            if len(data['password']) < 6:
                count = -1
                break
            elif not re.search("[a-z]", data['password']):
                count = -1
                break
            elif not re.search("[0-9]", data['password']):
                count = -1
                break
            elif re.search("\s", data['password']):
                count = -1
                break
            else:
                count = 0
                break
        if count == -1:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Password not valid must be contain alphabet and number minimum of 6 letters'
            }), 400
        pw_hash = encrypt(data['password'])
        company.password = pw_hash
    if 'company_name' in data:
        company.company_name = data['company_name']
    if 'website' in data:
        company.website = data['website']
    if 'profile_description' in data:
        company.profile_description = data['profile_description']
    if 'contact_number' in data:
        company.contact_number = data['contact_number']
    if 'address' in data:
        company.address = data['address']
    if 'city' in data:
        company.city = data['city']
    db.session.commit()
    return jsonify({
        'id': company.id, 'password': company.password, 'email': company.email, 'company_name': company.company_name,
        'website': company.website, 'profile_description': company.profile_description, 'contact_number': company.contact_number,
        'address': company.address, 'city': company.city, 'registration_date': company.registration_date
    })

###### CREATE USER EDUCATION ######
@app.route('/users/education-details/', methods=['POST'])
def create_education():
    email, password = login()
    u = Users.query.filter_by(email=email).first()
    if u is None or not bcrypt.check_password_hash(u.password, password):
        return {'error': 'Login Error'}, 401
    
    data = request.get_json()
    # if 'user_id' not in data: return {'message': 'User id must given'}, 400
    if 'level_education' not in data: return {'message': 'Level education not given'}, 400
    if 'major' not in data: return {'message': 'Major not given'}, 400
    if 'univ_name' not in data: return {'message': 'University name not given'}, 400
    if 'start_date' not in data: return {'message': 'Start date not given'}, 400
    if 'complete_date' not in data: return {'message': 'Complete date not given'}, 400
    if 'gpa' not in data: return {'message': 'GPA not given'}, 400

    edu = EducationDetail(
        user_id = u.id,
        last_education = data['level_education'],
        major = data['major'],
        univ_name = data['univ_name'],
        start_date = data['start_date'],
        complete_date = data['complete_date'],
        gpa = data['gpa']
    )
    db.session.add(edu)
    db.session.commit()
    
    return jsonify(
        {
            'id': edu.uedu.id,
            'first_name': edu.uedu.first_name,
            'last_name': edu.uedu.last_name,
            'date_of_birth': edu.uedu.date_of_birth,
            'gender': edu.uedu.gender
        },
        [{
            'level_education': ed.last_education,
            'major': ed.major,
            'univ_name': ed.univ_name,
            'start_date' : ed.start_date,
            'complete_date' : ed.complete_date,
            'gpa' : ed.gpa
        } for ed in EducationDetail.query.filter_by(user_id=edu.uedu.id)]
    )

###### CREATE USER EXPERIENCE ######
@app.route('/users/experience-details/', methods=['POST'])
def create_experience():
    email, password = login()
    u = Users.query.filter_by(email=email).first()
    if u is None or not bcrypt.check_password_hash(u.password, password):
        return {'error': 'Login Error'}, 401
    
    data = request.get_json()
    # if 'user_id' not in data: return {'message': 'User id must given'}, 400
    if 'job_title' not in data: return {'message': 'Job title not given'}, 400
    if 'company_name' not in data: return {'message': 'Company name not given'}, 400
    if 'job_location_city' not in data: return {'message': 'Job location city not given'}, 400
    if 'description_job' not in data: return {'message': 'Description job not given'}, 400
    if 'start_date' not in data: return {'message': 'Start date not given'}, 400
    if 'end_date' not in data: return {'message': 'End date not given'}, 400
    
    exp = ExperienceDetail(
        user_id = u.id,
        job_title = data['job_title'],
        company_name = data['company_name'],
        job_location_city = data['job_location_city'],
        description_job = data['description_job'],
        start_date = data['start_date'],
        end_date = data['end_date']
    )
    db.session.add(exp)
    db.session.commit()
    return jsonify(
        {
            'id': exp.uexp.id,
            'first_name': exp.uexp.first_name,
            'last_name': exp.uexp.last_name,
            'date_of_birth': exp.uexp.date_of_birth,
            'gender': exp.uexp.gender 
        },
        [{
            'job_title': ex.job_title,
            'company_name': ex.company_name,
            'job_location_city': ex.job_location_city,
            'start_date' : ex.start_date,
            'end_date' : ex.end_date,
            'description_job' : ex.description_job
        } for ex in ExperienceDetail.query.filter_by(user_id=exp.uexp.id)]
    )

###### POST A JOB ######
@app.route('/companies/post-job/', methods=['POST'])
def create_job_post():
    email, password = login()
    c = Company.query.filter_by(email=email).first()
    if c is None or not bcrypt.check_password_hash(c.password, password):
        return {'error': 'Login Error'}, 401
    
    data = request.get_json()
    jp = JobPost(
        company_id = c.id,
        title = data['title'],
        location_city = data['location_city'],
        job_description = data['job_description'],
        specialization = data['specialization']
    )
    db.session.add(jp)
    db.session.commit()

    return jsonify(
        {
            'id': jp.jpcom.id, 'company_name': jp.jpcom.company_name
        },
        [{
            'id': j.id, 'title': j.title, 'created_date': j.created_date, 'is_active': j.is_active,
            'job_description': j.job_description, 'location_city': j.location_city, 'specialization': j.specialization,
        } for j in JobPost.query.filter_by(company_id=jp.jpcom.id)]
    )

###### GET ALL JOB COMPANIES ######
@app.route('/companies/job-lists/')
def get_jobs_company():
    email, password = login()
    c = Company.query.filter_by(email=email).first()
    if c is None or not bcrypt.check_password_hash(c.password, password):
        return {'error': 'Login Error'}, 401
    return jsonify([
        {
        'id': jp.id, 'title': jp.title, 'created_date': jp.created_date, 'is_active': jp.is_active,
        'job_description': jp.job_description, 'location_city': jp.location_city, 'specialization': jp.specialization,
        'company': {
            'id': jp.jpcom.id,
            'company_name': jp.jpcom.company_name,
            'website': jp.jpcom.website
            }
        } for jp in JobPost.query.all()
    ])

###### GET A JOB COMPANIES ###### BY ID
@app.route('/companies/job-lists/<id>')
def get_job_company(id):
    email, password = login()
    c = Company.query.filter_by(email=email).first()
    if c is None or not bcrypt.check_password_hash(c.password, password):
        return {'error': 'Login Error'}, 401
    
    print(id)
    jp = JobPost.query.filter_by(id=id).first_or_404()
    return {
        'id': jp.id, 'title': jp.title, 'created_date': jp.created_date, 'is_active': jp.is_active,
        'job_description': jp.job_description, 'location_city': jp.location_city, 'specialization': jp.specialization,
        'company': {
            'id': jp.jpcom.id,
            'company_name': jp.jpcom.company_name,
            'website': jp.jpcom.website
            }
        }

###### EDIT A JOB COMPANIES ###### BY ID
@app.route('/companies/job-lists/<id>', methods=['PUT'])
def update_job_company(id):
    email, password = login()
    c = Company.query.filter_by(email=email).first()
    if c is None or not bcrypt.check_password_hash(c.password, password):
        return {'error': 'Login Error'}, 401
    
    data = request.get_json()
    jp = JobPost.query.filter_by(id=id).first_or_404()
    if 'title' in data:
        jp.title = data['title']
    if 'is_active' in data:
        jp.is_active = data['is_active']
    if 'job_description' in data:
        jp.job_description = data['job_description']
    if 'specialization' in data:
        jp.specialization = data['specialization']
    if 'location_city' in data:
        jp.location_city = data['location_city']
    db.session.commit()
    
    return {
        'id': jp.id, 'title': jp.title, 'created_date': jp.created_date, 'is_active': jp.is_active,
        'job_description': jp.job_description, 'location_city': jp.location_city, 'specialization': jp.specialization,
        'company': {
            'id': jp.jpcom.id,
            'company_name': jp.jpcom.company_name,
            'website': jp.jpcom.website
            }
        }

###### GET ALL AVAILABLE JOBS USER ######
@app.route('/users/job-lists/')
def get_jobs_users():
    # email, password = login()
    # u = Users.query.filter_by(email=email).first()
    # if u is None or not bcrypt.check_password_hash(u.password, password):
    #     return {'error': 'Login Error'}, 401
    
    return jsonify([
        {
            'id': jp.id,
            'title': jp.title,
            'created_date': jp.created_date,
            'job_description': jp.job_description,
            'is_active': jp.is_active,
            'location_city': jp.location_city,
            'specialization': jp.specialization,
            'company': {
                'company_name': jp.jpcom.company_name,
                'website': jp.jpcom.website,
                'profile_description': jp.jpcom.profile_description
            }
        } for jp in JobPost.query.filter_by(is_active = True)
    ])

###### FILTERING JOB USER BASED TITLE or SPECIALIZATION, LOCATION ######
@app.route('/users/filter-job-lists/')
def get_filter():
    data = request.get_json()
    dbQuery = db.session.query(JobPost)
    if (data['keywords'] != "" and data['location_city'] == ""):
        dbQuery = dbQuery.filter(or_(JobPost.title.match(data['keywords']), JobPost.specialization.match(data['keywords'])))
    elif (data["keywords"] == "" and data['location_city'] != ""):
        dbQuery = dbQuery.filter(JobPost.location_city.match(data['location_city']))
    elif (data['keywords'] != "" and data['location_city'] != ""):
        dbQuery = dbQuery.filter(JobPost.title.match(data['keywords']), JobPost.location_city.match(data['location_city']))
    else:
        dbQuery = dbQuery.all()
    return jsonify([
        {
        'id': jp.id, 'title': jp.title, 'created_date': jp.created_date, 'is_active': jp.is_active,
        'job_description': jp.job_description, 'location_city': jp.location_city, 'specialization': jp.specialization,
        'company': {
            'id': jp.jpcom.id,
            'company_name': jp.jpcom.company_name,
            'website': jp.jpcom.website
            }
        } for jp in dbQuery
    ])


###### SEARCH JOB USER BASED TITLE ######
@app.route('/users/job-lists/title/<id>')
def get_job_users_title(id):
    email, password = login()
    u = Users.query.filter_by(email=email).first()
    if u is None or not bcrypt.check_password_hash(u.password, password):
        return {'error': 'Login Error'}, 401
    
    print(id)
    return jsonify([
        {
        'id': jp.id, 'title': jp.title, 'created_date': jp.created_date, 'is_active': jp.is_active,
        'job_description': jp.job_description, 'location_city': jp.location_city, 'specialization': jp.specialization,
        'company': {
            'id': jp.jpcom.id,
            'company_name': jp.jpcom.company_name,
            'website': jp.jpcom.website
            }
        } for jp in db.session.query(JobPost).filter(JobPost.title.match(id))
    ])

###### SEARCH JOB USER BASED LOCATION ######
@app.route('/users/job-lists/location/<id>')
def get_job_users_location(id):
    email, password = login()
    u = Users.query.filter_by(email=email).first()
    if u is None or not bcrypt.check_password_hash(u.password, password):
        return {'error': 'Login Error'}, 401
    print(id)
    return jsonify([
        {
        'id': jp.id, 'title': jp.title, 'created_date': jp.created_date, 'is_active': jp.is_active,
        'job_description': jp.job_description, 'location_city': jp.location_city, 'specialization': jp.specialization,
        'company': {
            'id': jp.jpcom.id,
            'company_name': jp.jpcom.company_name,
            'website': jp.jpcom.website
            }
        } for jp in db.session.query(JobPost).filter(JobPost.location_city.match(id))
    ])

###### SEARCH JOB USER BASED SPECIALIZATION ######
@app.route('/users/job-lists/specialization/<id>')
def get_job_users_specialization(id):
    email, password = login()
    u = Users.query.filter_by(email=email).first()
    if u is None or not bcrypt.check_password_hash(u.password, password):
        return {'error': 'Login Error'}, 401
    print(id)
    return jsonify([
        {
        'id': jp.id, 'title': jp.title, 'created_date': jp.created_date, 'is_active': jp.is_active,
        'job_description': jp.job_description, 'location_city': jp.location_city, 'specialization': jp.specialization,
        'company': {
            'id': jp.jpcom.id,
            'company_name': jp.jpcom.company_name,
            'website': jp.jpcom.website
            }
        } for jp in db.session.query(JobPost).filter(JobPost.specialization.match(id))
    ])

###### GET A JOB DETAIL USER BY ID ######
@app.route('/users/job-lists/<id>')
def get_job_users(id):
    email, password = login()
    u = Users.query.filter_by(email=email).first()
    if u is None or not bcrypt.check_password_hash(u.password, password):
        return {'error': 'Login Error'}, 401
    
    print(id)
    jp = JobPost.query.filter_by(id=id).first_or_404()
    return {
        'id': jp.id, 'title': jp.title, 'created_date': jp.created_date, 'is_active': jp.is_active,
        'job_description': jp.job_description, 'location_city': jp.location_city, 'specialization': jp.specialization,
        'company': {
            'id': jp.jpcom.id,
            'company_name': jp.jpcom.company_name,
            'website': jp.jpcom.website
            }
        }

###### APPLY JOB USER ######
@app.route('/users/apply-job/', methods=['POST'])
def apply_job():
    email, password = login()
    u = Users.query.filter_by(email=email).first()
    if u is None or not bcrypt.check_password_hash(u.password, password):
        return {'error': 'Login Error'}, 401
    
    data = request.get_json()
    if not 'user_id' or not 'job_post_id' in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'User id and job post id must given'
        }), 400
    
    f = JobPostActivity.query.filter_by(user_id=u.id, job_post_id=data['job_post_id'])
    for i in f:
        if i is not None:
            return {'messages': 'You have applied this job'}, 400

    ap = JobPostActivity(
        user_id = u.id,
        job_post_id = data['job_post_id']
    )
    db.session.add(ap)
    db.session.commit()
    return {
        '1. messages': 'Success apply job',
        '2. title': ap.jpact.title,
        '3. company': ap.jpact.jpcom.company_name,
        '4. location_city': ap.jpact.location_city,
        '5. apply_date': ap.apply_date
    }, 201

###### DELETE APPLIED JOB USER ######
@app.route('/users/apply-job/<id>/', methods=['DELETE'])
def delete_apply_job(id):
    email, password = login()
    u = Users.query.filter_by(email=email).first()
    if u is None or not bcrypt.check_password_hash(u.password, password):
        return {'error': 'Login Error'}, 401
    
    f = JobPostActivity.query.filter_by(id=id).first_or_404()
    db.session.delete(f)
    db.session.commit()
    return {
        'success': 'Data deleted successfully'
    }

###### LIST APPLIED JOB USER ######
@app.route('/users/apply-job/<id>/')
def get_applied_job(id):
    email, password = login()
    u = Users.query.filter_by(email=email).first()
    if u is None or not bcrypt.check_password_hash(u.password, password):
        return {'error': 'Login Error'}, 401
    
    jp = JobPostActivity.query.filter_by(user_id=id).first()
    return jsonify(
        {
            'id': jp.user_id, 'first_name': jp.jpactivity.first_name, 'last_name': jp.jpactivity.last_name,
        },
        [{
            'title': jpa.jpact.title,
            'company': jpa.jpact.jpcom.company_name,
            'location_city': jpa.jpact.location_city,
            'apply_date': jpa.apply_date,
            'is_active': jpa.jpact.is_active
        } for jpa in JobPostActivity.query.filter_by(user_id=id)
    ])

###### GET DETAIL JOBSEEKER PROFILE FOR COMPANY ######
@app.route('/companies/get-users/<id>/')
def get_detail_user(id):
    email, password = login()
    c = Company.query.filter_by(email=email).first()
    if c is None or not bcrypt.check_password_hash(c.password, password):
        return {'error': 'Login Error'}, 401
    
    print(id)
    u = Users.query.filter_by(id=id).first_or_404()

    return jsonify(
        {
            'id' : u.id, 'first_name': u.first_name, 'last_name': u.last_name,
            'date_of_birth': u.date_of_birth, 'gender': u.gender, 'email': u.email,
            'contact number': u.contact_number
        },
        {'education':
            [{
            'level_education': edu.last_education, 'major': edu.major, 'univ_name': edu.univ_name,
            'start_date': edu.start_date, 'complete_date': edu.complete_date, 'gpa': edu.gpa
        } for edu in EducationDetail.query.filter_by(user_id=id)]},
        {'experience':
        [{
            'job_title': exp.job_title, 'company_name': exp.company_name, 'job_location_city': exp.job_location_city,
            'description_job': exp.description_job, 'start_date': exp.start_date, 'end_date': exp.end_date
        } for exp in ExperienceDetail.query.filter_by(user_id=id)
        ]})
    
###### LIST ALL APLICANT ON JOB FOR COMPANY ######
@app.route('/companies/job-lists/get-users/<id>/')
def get_users_job(id):
    email, password = login()
    c = Company.query.filter_by(email=email).first()
    if c is None or not bcrypt.check_password_hash(c.password, password):
        return {'error': 'Login Error'}, 401
    print(id)
    jp = JobPost.query.filter_by(id=id).first_or_404()

    return jsonify(
        {'job_post':
        {
            'id': jp.id, 'title': jp.title, 'company_name': jp.jpcom.company_name,
            'location_city': jp.location_city
        }},
        {'aplicant':
        [{
            'id': jpa.jpactivity.id, 'email': jpa.jpactivity.email, 'first_name': jpa.jpactivity.first_name,
            'last_name': jpa.jpactivity.last_name, 'apply_date': jpa.apply_date
        } for jpa in JobPostActivity.query.filter_by(job_post_id=id)]}
    )

###### LIST ALL JOB WITH TOTAL APLICANT FOR COMPANY ######
@app.route('/companies/job-lists/count/')
def get_jobs_count_company():
    email, password = login()
    c = Company.query.filter_by(email=email).first()
    if c is None or not bcrypt.check_password_hash(c.password, password):
        return {'error': 'Login Error'}, 401
    
    return jsonify([
        {
            '1. job_post_id': jp.id, '2. title': jp.title, '3. company_name': jp.jpcom.company_name, '4. specialization': jp.specialization,
            '5. location_city': jp.location_city,
            '6. total_applicant': JobPostActivity.query.filter_by(job_post_id=jp.id).count()
        } for jp in JobPost.query.all()
    ])

@app.route('/company/login/', methods=['POST'])
def company_login():
    res = request.headers.get("Authorization")
    a = res.split()
    u = base64.b64decode(a[-1]).decode('utf-8')
    mail, passw = u.split(":")

    c = Company.query.filter_by(email=mail).first()
    if c is None or not bcrypt.check_password_hash(c.password, passw):
        return {'error': 'Login Error'}, 401

    else:
        return {
        'email' : mail
        }

@app.route('/user/login/', methods=['POST'])
def user_login():
    res = request.headers.get("Authorization")
    a = res.split()
    u = base64.b64decode(a[-1]).decode('utf-8')
    mail, passw = u.split(":")

    c = Users.query.filter_by(email=mail).first()
    if c is None or not bcrypt.check_password_hash(c.password, passw):
        return {'error': 'Login Error'}, 401

    else:
        return {
        'email' : mail
        }


@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'POST,GET,PUT,DELETE,OPTION')
  return response