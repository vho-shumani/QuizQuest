"""Module contain create_app function which created flask application"""
from flask import Flask
import os


def create_app():
    """ Create and manages a Flask application
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or \
        '648168738ED817547FC7A2D2CE2C9'

    return app
