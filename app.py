"""module runs the flask apllication
"""
from quiz_app import create_app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)