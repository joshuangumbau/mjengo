from __main__ import app 
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

# Initialize the app and db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your-secret-key'
db = SQLAlchemy(app)

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    nationalid = db.Column(db.Integer, unique=True, nullable=False)
    phonenumber = db.Column(db.Integer, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

class jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numberofworkers = db.Column(db.Integer, nullable=False)
    companyname = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(80), nullable=False)
    jobdescription = db.Column(db.String(80), nullable=False)
    jobtype = db.Column(db.String(80), nullable=True)
    jobrequirements = db.Column(db.String(80), nullable=False)
    jobdeadline = db.Column(db.String(80), nullable=False)


with app.app_context():
    db.create_all()



#jobcreation
@app.route('/createjob', methods=['GET','POST'])
def jobcreation():
    if request.method == 'POST':
        companyname = request.form.get('companyname')
        location = request.form.get('location')
        numberofworkers = request.form.get('numberofworkers')
        jobdescription = request.form.get('jobdescription')
        jobtype = request.form.get('jobtype')
        jobrequirements = request.form.get('jobrequirements')
        jobdeadline = request.form.get('jobdeadline')

        new_job = jobs(companyname=companyname, location=location, numberofworkers=numberofworkers, jobdescription=jobdescription, jobtype=jobtype, jobrequirements=jobrequirements, jobdeadline=jobdeadline)
        db.session.add(new_job)
        db.session.commit()
    

        return render_template('jobs.html')

@app.route('/jobcreated')
def jobcreated():
    all_jobs = jobs.query.all()
    return render_template('jobscreated.html', jobs=all_jobs)
