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
                                     validators=[EqualTo('password',  message='Passwords must match')])
    submit = SubmitField('Sign Up')

class EditProfileForm(FlaskForm):
    """Form for editing user profile"""
    email = StringField('Email',
                       validators=[DataRequired(), Email()])
    current_password = PasswordField('Current Password',
                                     validators=[DataRequired()])
    new_password = PasswordField('New Password',
                                validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(
        'Confirm New Password',
        validators=[EqualTo('new_password', message='Passwords must match')])
    submit = SubmitField('Update Profile')
