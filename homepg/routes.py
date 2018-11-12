from flask import render_template, url_for, flash, redirect, request
from homepg import app, db, bcrypt
#from flaskblog.models import User, Post
#from flaskblog.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    pass

@app.route("/login", methods=['GET', 'POST'])
def login():
    pass

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    pass