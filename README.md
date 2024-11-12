# QuizQuest

## Introduction

QuizQuest is a Flask-based web application that provides an interactive platform for creating, managing, and taking quizzes. The application features user authentication, an admin panel for quiz management, and a RESTful API for accessing quiz data.

## Features
**User authentication system**
- User registration and login
- Secure password hashing using bcrypt
- Remember me functionality
- Admin privileges for administrator

**Quiz Management** (as admin)
- Create and mange quizzes through admin interface
- Add Multichoice questions 
- set quiz duration

**Admin Panel**
- Secure admin interface
- Manage users, quizzes, and questions
- View detailed information about users and quizzes

**Restful API**
- Endpoint to retrieve all quizzes
- Endpoint to retrieve specific quiz details
- JSON response format

## Technical stack
- Backend: Python (flask)
- Frontend: HTML, CSS
- Database: SQLAlchemy with SQLite
- Authentication: Flask-login and Flask-Bcrypt (password hashing)
- Admin panel: Flask-Admin
- API framework: Flask-Restful

## Installation
1. Clone repository

```bash
git clone https://github.com/vho-shumani/QuizQuest.git
cd QuizQuest
```


2. Setup virtual environment

```bash
python -m venv venv
source venv/bin/activate  
```

3. Install dependencies

```
pip install -r requirements.txt
```

4. Set up environment variables (optional)

```
export SECRET_KEY='your-secret-key'
export DATABASE_URL='database-url'
```

## Usage

- Run application
```
flask run
```
- Access the application at http://localhost:5000
- Create an admin account by registering with the username 'admin'
- Access the admin panel at /admin, where you can add, edit, and delete quizzes and questions.

- Visit the /signup route to create a new user account.
- Visit the /login route to log in to the application.

- After logging in, navigate to the /categories route to view the available quiz categories.
- Click on a category to see the list of quizzes.
- Click on a quiz to start taking it.

- After completing a quiz, the results will be displayed, and you can choose to save your score.
- Visit the /profile route to view your quiz history and statistics.

## API endpoints
- `GET /api/quizzes` : Retrieve list of all quizzes
- `GET /api/quizzes/<quiz_id>` : Retrieve specific quiz details including questions

## License
This project is licensed under the MIT License. See the LICENSE file for details.