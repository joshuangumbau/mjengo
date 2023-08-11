from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)



import jobs

import login

if __name__ == '__main__':
    app.run(debug=True)
