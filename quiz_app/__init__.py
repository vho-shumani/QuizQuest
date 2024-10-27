"""Module contain create_app function which created flask application"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


db = SQLAlchemy()


def create_app():
    """ Create and manages a Flask application
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or \
        '648168738ED817547FC7A2D2CE2C9'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
        'sqlite:///users.db'
    
    db.init_app(app)
    
    from .route import views
    app.register_blueprint(views, url_prefix="/")

    with app.app_context():
        db.create_all()

    return app
