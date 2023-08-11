from __main__ import app
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from jobs import users
from jobs import db
from jobs import jobs

# signup page
@app.route('/')
def index():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    nationalid = request.form.get('nationalid')
    phonenumber = request.form.get('phonenumber')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')    
    password = request.form.get('password')
    
    hashed_password = generate_password_hash(password, method='sha256')
    new_user = users(firstname=firstname, lastname=lastname, password_hash=hashed_password, phonenumber=phonenumber, nationalid=nationalid)
    
    db.session.add(new_user)
    db.session.commit()
    
    return redirect(url_for('index'))  

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nationalid = request.form.get('nationalid')  
        password = request.form.get('password')

        user = users.query.filter_by(nationalid=nationalid).first()

        if user and check_password_hash(user.password_hash, password):
            # Successful login
            session['id'] = user.id
            all_jobs = jobs.query.all()  # Fetch all jobs

            return render_template('jobscreated.html', jobs = all_jobs)
            

        else:
            # Failed login
            return render_template('failedlogin.html')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))