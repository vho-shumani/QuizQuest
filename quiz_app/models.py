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
