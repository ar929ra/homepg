from flask import render_template, url_for, flash, redirect, request
from homepg import app, db, bcrypt
from homepg.models import User, Household, Activity
from homepg.forms import RegistrationForm, LoginForm, CreateHome
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/my_home", methods=['GET', 'POST'])
def my_home():
    if not current_user.is_authenticated:
        return redirect(url_for('home.html'))

    this_user = User.query.filter_by(email = current_user.email).first()

    form = CreateHome()
    if form.validate_on_submit():
        home = Household(name = form.name.data)
        this_user.households.append(home)
        db.session.commit()

    household_len = len(this_user.households)
    activities = this_user.activities

    return render_template(
        'my_home.html', 
        household = household_len, 
        form = form,
        activities = activities
    )

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(username = form.username.data, email = form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('my_home'))

    form = LoginForm()
    if form.validate_on_submit():
        user= User.query.filter_by(email = form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('my_home'))

        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)

@app.route("/record_activity", methods=['POST'])
def record_activity():
    if request.method == "POST":

        activity_name = request.form['activity_name']
        activity_desc = request.form['activity_desc']

        this_user = User.query.filter_by(email = current_user.email).first()

        activity = Activity(name = activity_name, description = activity_desc)
        this_user.activities.append(activity)
        db.session.commit()

        return "Submitted activity"

    return redirect(url_for('my_home'))

@app.route("/delete_activity", methods=['POST'])
def delete_activity():
    if request.method == "POST":

        activity_name = request.form['activity_name'].lower().strip().replace("\n","").replace("\t","")
        this_user_id = current_user.id
        
        db.engine.execute(
            "DELETE FROM activity WHERE user_id = {0} AND lower(name) = \'{1}\'".format(
                this_user_id, activity_name) 
        )
        db.session.commit()

        return "Removed activity"

    return redirect(url_for('my_home'))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    pass