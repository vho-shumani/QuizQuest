"""Module consist of forms for user authentication"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    """Implements user login with all the required fields"""
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=8)])
    login = SubmitField('Login')
    remember_me = BooleanField('Remenber me')


class RegistrationForm(FlaskForm):
    """handles user registration form"""
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=5, max=15)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm password',
                                     validators=[EqualTo('password')])
    submit = SubmitField('Sign Up')
