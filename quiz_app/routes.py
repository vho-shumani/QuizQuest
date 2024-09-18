"""Module consist of routes/views for application"""
from flask import Blueprint, render_template, flash, request, redirect, url_for
from .forms import LoginForm
from flask_login import current_user, login_user
from .models import User
from . import bcrypt


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
        return redirect(url_for('home'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash(f'Welcome back {user.username}', 'success')
            return redirect(next_page) if next_page else redirect(url_for('/'))
        else:
            print('here')
            flash('Login Unsuccessful. Please check email and/or password', 'error')
    return render_template('login.html', form=form)

