"""Module consist of application of route"""
from flask import Blueprint 


views = Blueprint('views', __name__)


@views.route('/')
def index():
    """Handles the root url('/')"""
    return 'hello'
