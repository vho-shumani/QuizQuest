"""Module consist of forms for user authentication"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
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


class QuestionForm(FlaskForm):
    """handles questions for quizes"""
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    text = StringField('Question', validators=[DataRequired()])
    option1 = StringField('1:', validators=[DataRequired()])
    option2 = StringField('2:', validators=[DataRequired()])
    option3 = StringField('3:', validators=[DataRequired()])
    correct_answer = SelectField('Answer', choices=[
        ('option1', '1'),
        ('option2', '2'),
        ('option3', '3')
    ])
    add = SubmitField('Submit')
