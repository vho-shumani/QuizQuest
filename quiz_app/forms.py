"""Module consist of forms for user authentication"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email

class LoginForm(FlaskForm):
    """Implements user login with all the required fields"""
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                             validators=[DataRequired(), Length(min=8)])
    login = SubmitField('Login')
    remember_me = BooleanField('Remenber me')
