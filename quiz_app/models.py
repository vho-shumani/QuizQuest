"""Module consist of models"""
from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    """Handles User schema"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"User('{self.username}-{self.id}')"

class Quiz(db.Model):
    """The schema for the quizes"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(200), unique=True, nullable=False)
    Time = db.Column(db.Integer, nullable=False)
    questions = db.relationship('Question', backref='quiz', lazy=True)

    def __repr__(self):
        return f"Quiz('{self.title}-{self.id}')"

class Question(db.Model):
    """schema for the questions for specific quiz"""
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    option1 = db.Column(db.String(120), nullable=False)
    option2 = db.Column(db.String(120), nullable=False)
    option3 = db.Column(db.String(120), nullable=False)
    correct_answer = db.Column(db.String(100), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)

    def __repr__(self):
        return f"Question('{self.text}-{self.id}')"
