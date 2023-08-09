from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
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
@app.route('/jobs', methods=['POST'])
def jobcreation():
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
    return redirect(url_for('jobcreated'))

@app.route('/jobcreated')
def jobcreated():
    all_jobs = jobs.query.all()
    return render_template('jobscreated.html', jobs=all_jobs)



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
            session['user_id'] = user.id
            return render_template('jobs.html')
        else:
            # Failed login
            return "Login failed."

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
