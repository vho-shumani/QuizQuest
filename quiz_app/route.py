"""Module consist of application of route"""
from flask import Blueprint, render_template, flash, redirect, request, url_for
from .form import LoginForm, RegistrationForm
from flask_login import login_user, logout_user, login_required
from .models import User
from . import bcrypt, db


views = Blueprint('views', __name__)


@views.route('/')
def index():
    """Handles the root url('/')"""
    return render_template('base.html')


@views.route('/login', methods=['GET', 'POST'])
def login():
    """Handles the login url('/login')"""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and \
          bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash(f'Welcome Back {user.username}', 'success')
            redirect_url = next_page if next_page else url_for('views.index')
            return redirect(redirect_url)
        else:
            flash("""Login unsuccessful, 
                Please check email and/or password""", 'danger')
    return render_template('login.html', form=form)


@views.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handles the signup url('/signup')"""
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        email = User.query.filter_by(email=form.email.data).first()
        if user is None and email is None:
            hashed_pass = bcrypt.generate_password_hash(form.password.data)
            user = User(username=form.username.data, email=form.email.data,
                        password=hashed_pass)
            db.session.add(user)
            db.session.commit()
            flash(f'''Account successfully created 
                for {form.username.data}''', 'success')
            return redirect(url_for('views.login'))
        else:
            if user and email:
                flash(f'''{form.username.data}
                      and {form.email.data} already exist''', 'error')
            elif user:
                flash(f'{form.username.data} exists', 'danger')
            elif email:
                flash(f'{form.email.data} exists', 'danger')
    elif request.method == 'POST':
        flash('Error occurred creating account', 'danger')
    return render_template('signup.html', form=form)

@views.route('/logout')
@login_required
def logout():
    """handles logout of user"""
    logout_user()
    return redirect(url_for('views.login'))
