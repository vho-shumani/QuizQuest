"""Module consist of application of route"""
from flask import Blueprint, render_template, flash, redirect, request
from .form import LoginForm, RegistrationForm
from flask_login import login_user
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
    return render_template('sign.html')