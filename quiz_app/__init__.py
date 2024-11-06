"""Module contain create_app function which created flask application"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin
import os


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
admin = Admin(name="QUIZQUEST", template_mode="bootstrap4")


def create_app():
    """ Create and manages a Flask application
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or \
        '648168738ED817547FC7A2D2CE2C9'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
        'sqlite:///users.db'
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    from .models import SecureAdminView
    admin.init_app(app, index_view=SecureAdminView())
    
    from .route import views
    app.register_blueprint(views)

    login_manager.login_view = 'views.login'

    from .models import setup_admin, User, Quiz, Question
    with app.app_context():
        db.create_all()
        setup_admin()

    @login_manager.user_loader
    def load_user(user_id):
        """ Reload the user object from the user ID stored in the session"""
        from .models import User
        return User.query.get(int(user_id))

    return app
