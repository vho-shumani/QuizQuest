"""Module consist of application of route"""
from flask import Blueprint, render_template, flash, redirect, request, url_for, session
from .form import LoginForm, RegistrationForm
from flask_login import login_user, logout_user, login_required
from .models import User, Quiz, Question
from . import bcrypt, db
import time


views = Blueprint('views', __name__)


@views.route('/')
def index():
    """Handles the root url('/')"""
    return render_template('index.html')


@views.route('/login', methods=['GET', 'POST'])
def login():
    """Handles the login url('/login')"""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and \
          bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash(f'Welcome Back {user.username}', 'success')
            redirect_url = next_page if next_page else url_for('views.index')
            return redirect(redirect_url)
        else:
            flash("""Login unsuccessful, 
                Please check email and/or password""", 'danger')
    return render_template('login.html', form=form)


@views.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handles the signup url('/signup')"""
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        email = User.query.filter_by(email=form.email.data).first()
        if user is None and email is None:
            hashed_pass = bcrypt.generate_password_hash(form.password.data)
            if form.username.data == 'admin':
                user = User(username=form.username.data,
                            email=form.email.data,
                            password=hashed_pass,
                            is_admin=True)
            else:
                user = User(username=form.username.data,
                            email=form.email.data,
                            password=hashed_pass,
                            is_admin=False)
            db.session.add(user)
            db.session.commit()
            flash(f'''Account successfully created 
                for {form.username.data}''', 'success')
            return redirect(url_for('views.login'))
        else:
            if user and email:
                flash(f'''{form.username.data}
                      and {form.email.data} already exist''', 'error')
            elif user:
                flash(f'{form.username.data} exists', 'danger')
            elif email:
                flash(f'{form.email.data} exists', 'danger')
    elif request.method == 'POST':
        flash('Error occurred creating account', 'danger')
    return render_template('signup.html', form=form)

@views.route('/logout')
@login_required
def logout():
    """handles logout of user"""
    logout_user()
    return redirect(url_for('views.login'))

@views.route('/categories')
@login_required
def categories():
    """Handles categories page"""


@views.route('/quizes')
@login_required
def quizes():
    """Handles the quiz url"""
    page = request.args.get('page', 1, type=int)
    per_page = 6
    quizes = Quiz.query.paginate(
        page=page,
        per_page=per_page,
        error_out=False)
    return render_template('quizes.html', quizes=quizes)

@views.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def quiz(quiz_id):
    """Handles the quiz page/url"""
    page = request.args.get('page', 1, type=int)
    per_page = 1
    quiz = Quiz.query.filter_by(id=quiz_id).first()
    TOTAL_QUIZ_TIME = quiz.duration * 60 
    questions = Question.query.filter_by(quiz_id=quiz_id).paginate(
        page=page,
        per_page=per_page,
    )

    if f'quiz_answers' not in session:
        session[f'quiz_answers'] = {}


    if not questions.items:
        flash('No questions found for this quiz.', 'warning')
        return redirect(url_for('views.home'))

    if page == 1:
        session[f'quiz_start_time'] = time.time()
        session[f'quiz_time_limit'] = TOTAL_QUIZ_TIME

    start_time = session.get(f'quiz_start_time')
    time_limit = session.get(f'quiz_time_limit')
    
    if start_time:
        elapsed_time = time.time() - start_time
        remaining_time = max(0, time_limit - elapsed_time)
    else:
        remaining_time = time_limit

    if remaining_time <= 0:
        score = 0
        num_correct = 0
        stored_answers = session.get(f'quiz_answers', {})
        all_questions = Question.query.filter_by(quiz_id=quiz_id).all()
        for question in all_questions:
            if str(question.id) in stored_answers:
                if question.correct_answer == stored_answers[str(question.id)]:
                    score += 10
                    num_correct += 1
        
        num_incorrect = len(all_questions) - num_correct
        session.pop(f'quiz_answers', None)
        session.pop(f'quiz_start_time', None)
        session.pop(f'quiz_time_limit', None)

        flash('Time is up! Quiz submitted automatically.', 'warning')
        return redirect(url_for('views.results', 
                                quiz_id=quiz_id, 
                                score=score,
                                num_incorrect=num_incorrect,
                                num_correct=num_correct, 
                                total_questions=len(all_questions)))

    if request.method == 'POST':
        for question in questions.items:
            selected_answer = request.form.get(str(question.id))
            if selected_answer:
                session[f'quiz_answers'][str(question.id)] = selected_answer
                session.modified = True

        if page == questions.pages:
            score = 0
            num_correct = 0
            stored_answers = session.get(f'quiz_answers', {})
            all_questions = Question.query.filter_by(quiz_id=quiz_id).all()
            for question in all_questions:
                if str(question.id) in stored_answers:
                    if question.correct_answer == stored_answers[str(question.id)]:
                        score += 10
                        num_correct += 1
            
            num_incorrect = len(all_questions) - num_correct
            session.pop(f'quiz_answers', None)

            flash(f'Your score: {score}', 'success')
            return redirect(url_for('views.results', 
                                    quiz_id=quiz_id, 
                                    score=score,
                                    num_incorrect=num_incorrect,
                                    num_correct=num_correct, 
                                    total_questions=len(all_questions)))
        else:
            return redirect(url_for('views.quiz', quiz_id=quiz_id, page=page + 1))
    return render_template(
        'quiz.html',
        questions=questions,
        stored_answers=session.get(f'quiz_answers', {}),
        remaining_time=int(remaining_time)
    )

@views.route('/results')
def results():
    """Handle the results page"""
    score = request.args.get('score')
    remaining_time = request.args.get('remaining_time')
    quiz_id = request.args.get('quiz_id')
    total_questions = request.args.get('total_question')
    incorrect = request.args.get('num_incorrect')
    correct = request.args.get('num_correct')
    quiz = Quiz.query.filter_by(id=quiz_id).first()
    return render_template('results.html',
                            quiz_id=quiz_id,
                            score=score,
                            correct=correct,
                            incorrect=incorrect,
                            total_questions=total_questions,
                            quiz_title=quiz.title)
