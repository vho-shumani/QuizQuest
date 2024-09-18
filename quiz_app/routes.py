"""Module consist of routes/views for application"""
from flask import Blueprint, render_template, flash, request, redirect, url_for
from .forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user
from .models import User
from . import bcrypt, db


views = Blueprint('views', __name__)

@views.route('/')
def index():
    """Handles the root url('/') and renders the index.html(index page)"""
    return render_template('index.html')

@views.route('/login', methods=['GET', 'POST'])
def login():
    """Handles the login url('/login') and renders the login page"""
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('views.index'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash(f'Welcome back {user.username}', 'success')
            return redirect(next_page) if next_page else redirect(url_for('views.index'))
        else:
            flash('Login Unsuccessful. Please check email and/or password', 'error')
    return render_template('login.html', form=form)

@views.route('/signup', methods=['GET', 'POST'])
def sign():
    """Renders signup templates"""
    if current_user.is_authenticated:
        return redirect(url_for('views.index'))
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
            flash(f'Account successfully created for {form.username.data}', 'success')
            return redirect(url_for('views.login'))
        else:
            if user and email:
                flash(f'{form.username.data} and {form.email.data} already exist', 'error')
            elif user:
                flash(f'{form.username.data} exists', 'error')
            elif email:
                flash(f'{form.email.data} exists', 'error')
    elif request.method == 'POST':
        flash('Error occurred creating account', 'error')
    return render_template('signup.html', form=form)
