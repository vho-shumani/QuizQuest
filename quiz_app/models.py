"""Contains the SQLAlchemy models for the app"""
from . import db, admin
from flask import redirect, url_for, flash
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView


class User(db.Model, UserMixin):
    """Handles User schema"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    quiz_results = db.relationship("QuizResult", back_populates="user")

    def __repr__(self):
        return f"User: {self.username}"


class Category(db.Model):
    """Schema for quiz catergories"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    quizzes = db.relationship("Quiz", back_populates="category")

    def __repr__(self):
        return f"Category: {self.title}"


class Quiz(db.Model):
    """The schema for the quizes"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer,
                            db.ForeignKey('category.id'),
                            nullable=False)
    category = db.relationship("Category", back_populates="quizzes")
    questions = db.relationship("Question", back_populates="quiz")
    quiz_results = db.relationship("QuizResult", back_populates="quiz")

    def __repr__(self):
        return f"Quiz: {self.title}"


class Question(db.Model):
    """schema for the questions for specific quiz"""
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    option1 = db.Column(db.String(120), nullable=False)
    option2 = db.Column(db.String(120), nullable=False)
    option3 = db.Column(db.String(120), nullable=False)
    correct_answer = db.Column(db.String(100), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    quiz = db.relationship("Quiz", back_populates="questions")

    def __repr__(self):
        return f"Question:'{self.question}' quiz: {self.quiz}')"


class QuizResult(db.Model):
    """schema for the result for specific quiz"""
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer)
    incorrect = db.Column(db.Integer)
    correct = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    user = db.relationship("User", back_populates="quiz_results")
    quiz = db.relationship("Quiz", back_populates="quiz_results")

    def __repr__(self):
        return f"('{self.user}-{self.quiz}')"


class SecureModelView(ModelView):
    """
    A secure version of the Flask-Admin ModelView.

    This view checks if the current user is authenticated and an admin before
    allowing access to the model section of admin panel.
    """
    def is_accessible(self):
        if current_user.is_authenticated and current_user.is_admin:
            return True

    def inaccessible_callback(self, name, **kwargs):
        flash('Only administrator can access this page.', 'warning')
        return redirect(url_for('views.login', next=url_for('admin.index')))


class SecureAdminView(AdminIndexView):
    """
    A secure version of the Flask-Admin AdminIndexView.

    This view checks if the current user is authenticated and an admin before
    allowing access to the admin panel.
    """
    def is_accessible(self):
        if current_user.is_authenticated and current_user.is_admin:
            return True

    def inaccessible_callback(self, name, **kwargs):
        flash('Please log in with admin credentials', 'warning')
        return redirect(url_for('views.login', next=url_for('admin.index')))


class CatergoryAdminView(SecureModelView):
    """Customization view for category model"""
    column_list = ['id', 'title']
    form_columns = ['title', 'description']
    create_modal = True
    edit_modal = True
    can_edit = True
    can_view_details = True


class QuizAdminView(SecureModelView):
    """Customization view for quiz model"""
    column_list = ['id', 'title', 'description', 'duration', 'category']
    form_columns = ['title', 'description', 'duration', 'category_id']
    edit_modal = True
    can_edit = True
    can_view_details = True


class UserAdminView(SecureModelView):
    """Customization view for user model"""
    column_list = ['username', 'email']
    can_create = False
    can_edit = False
    can_view_details = True


class ResultAdminView(SecureModelView):
    """Customization view for results model"""
    column_list = ['score', 'user', 'quiz']
    can_create = False
    can_edit = False
    can_view_details = True


class QuestionAdminView(SecureModelView):
    """Customization view for question model"""
    column_list = ['question', 'quiz']
    form_columns = ['question',
                    'option1',
                    'option2',
                    'option3',
                    'correct_answer',
                    'quiz_id']
    edit_modal = True
    can_view_details = True


def setup_admin():
    """Setup admin views"""
    admin.add_view(UserAdminView(User, db.session))
    admin.add_view(CatergoryAdminView(Category, db.session))
    admin.add_view(QuizAdminView(Quiz, db.session))
    admin.add_view(QuestionAdminView(Question, db.session))
    admin.add_view(ResultAdminView(QuizResult, db.session))
