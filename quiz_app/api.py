"""Contains the API endpoints for the app"""
from .models import Quiz
from . import api
from flask_restful import Resource, fields, marshal_with


question_fields = {
    'id': fields.Integer,
    'question': fields.String,
    'option1': fields.String,
    'option2': fields.String,
    'option3': fields.String,
    'correct_answer': fields.String
}


class AllQuizzesResource(Resource):
    """Retrieves a list of all quizzes."""
    quizfields = {
        'id': fields.Integer,
        'title': fields.String,
        'description': fields.String,
        'duration': fields.Integer,
    }

    @marshal_with(quizfields)
    def get(self):
        """Retrieves list of all quizzes"""
        quizzes = Quiz.query.all()
        return quizzes


class QuizResource(Resource):
    """Retrieves specific quiz by id"""
    quizfields = {
        'id': fields.Integer,
        'title': fields.String,
        'description': fields.String,
        'duration': fields.Integer,
        'questions': fields.List(fields.Nested(question_fields))
    }

    @marshal_with(quizfields)
    def get(self, quiz_id):
        """Retrieves quiz with specidied id"""
        quiz = Quiz.query.filter_by(id=quiz_id).first()
        if not quiz:
            return {'message': 'Quiz not found'}, 404
        return quiz


api.add_resource(AllQuizzesResource, '/api/quizzes')
api.add_resource(QuizResource, '/api/quizzes/<int:quiz_id>')
