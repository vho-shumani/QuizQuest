"""Module consist of application of route"""
from flask import Blueprint, render_template


views = Blueprint('views', __name__)


@views.route('/')
def index():
    """Handles the root url('/')"""
    return render_template('base.html')
