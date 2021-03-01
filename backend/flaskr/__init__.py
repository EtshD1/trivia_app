from logging import error
import os
from flask import Flask, json, request, abort, jsonify
from sqlalchemy.orm import query
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import sys
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def paginate(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page-1) * QUESTIONS_PER_PAGE
    limit = start + QUESTIONS_PER_PAGE

    if limit > len(selection):
        limit = len(selection)

    pageList = []
    for count in range(start, limit):
        pageList.append(selection[count].format())

    if len(pageList) == 0:
        abort(404)

    db.session.close()

    return pageList


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    db.init_app(app)

    # TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs

    cors = CORS(app, resources={r'/api/*': {"origins": "*"}})

    # TODO:Done Use the after_request decorator to set Access-Control-Allow

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-METHODS',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    # @TODO:Done
    # Create an endpoint to handle GET requests
    # for all available categories.
    @app.route('/categories')
    def get_categories():
        try:
            query = Category.query.order_by(Category.id).all()
            if len(query) > 0:
                categories = [category.format() for category in query]
                return jsonify({'success': True, 'total_categories': len(categories), 'categories': categories})
            else:
                return jsonify({'success': False, 'error': 404, 'message': "Categories not found. Database might be empty."}), 404
        except:
            db.session.rollback()
            print(sys.exc_info())
            abort(500)
        finally:
            db.session.close()

    # TODO:Done
    # Create an endpoint to handle GET requests for questions,
    # including pagination (every 10 questions).
    # This endpoint should return a list of questions,
    # number of total questions, current category, categories.

    # TEST: At this point, when you start the application
    # you should see questions and categories generated,
    # ten questions per page and pagination at the bottom of the screen for three pages.
    # Clicking on the page numbers should update the questions.

    @app.route('/questions')
    def get_questions():
        try:
            query = Question.query.order_by(Question.id).all()

            questionList = paginate(request, query)

            return jsonify({'success': True, 'total_questions': len(query), 'questions': questionList})
        except:
            db.session.rollback()
            print(sys.exc_info())
            abort(500)
        finally:
            db.session.close()

    # @TODO:
    # Create an endpoint to DELETE question using a question ID.

    # TEST: When you click the trash icon next to a question, the question will be removed.
    # This removal will persist in the database and when you refresh the page.

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            query = Question.query.get(question_id)

            query.delete()

            allQuestionQuery = Question.query.all()

            return jsonify({'success': True, 'total_questions': len(allQuestionQuery)})
        except:
            db.session.rollback()
            print(sys.exc_info())
            abort(500)
        finally:
            db.session.close()

    # @TODO:
    # Create an endpoint to POST a new question,
    # which will require the question and answer text,
    # category, and difficulty score.

    # TEST: When you submit a question on the "Add" tab,
    # the form will clear and the question will appear at the end of the last page
    # of the questions list in the "List" tab.
    @app.route('/questions', methods=['POST'])
    def create_questions():
        try:
            body = request.get_json()

            question = body.get('question')
            category = body.get('category')
            difficulty = body.get('difficulty', None)
            answer = body.get('answer', None)
            if question and category:
                newQuestion = Question(
                    question=question, category=category, difficulty=difficulty, answer=answer)
                newQuestion.insert()
                allQuestionQuery = Question.query.all()
                return jsonify({'success': True, 'total_questions': len(allQuestionQuery), 'question': newQuestion.format()})
            else:
                abort(400)
        except:
            db.session.rollback()
            print(sys.exc_info())
            abort(500)
        finally:
            db.session.close()

    # @TODO:
    # Create a POST endpoint to get questions based on a search term.
    # It should return any questions for whom the search term
    # is a substring of the question.

    # TEST: Search by any phrase. The questions list will update to include
    # only question that include that string within their question.
    # Try using the word "title" to start.
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        try:
            search_term = request.get_json().get("search_term")
            query = Question.query.filter(Question.question.ilike(
                "%"+search_term+"%")).order_by(Question.id).all()
            questions = [question.format() for question in query]
            return jsonify({"success": True, "total_matches": len(questions), "questions": questions})
        except:
            db.session.rollback()
            print(sys.exc_info())
            abort(500)
        finally:
            db.session.close()

    # @TODO:
    # Create a GET endpoint to get questions based on category.

    # TEST: In the "List" tab / main screen, clicking on one of the
    # categories in the left column will cause only questions of that
    # category to be shown.
    @app.route('/categories/<int:cat_id>')
    def find_by_category(cat_id):
        try:
            category_query = Category.query.get(cat_id)
            name = category_query.type
            if category_query:

                questionQuery = Question.query.filter(
                    Question.category == name).order_by(Question.id).all()
                questions = []

                for q in questionQuery:
                    question = q.format()
                    question.pop("category")
                    questions.append(question)

                return jsonify({
                    "success": True,
                    "category": name,
                    "questions": questions
                })

            else:
                abort(404)
        except:
            db.session.rollback()
            print(sys.exc_info())
            abort(500)
        finally:
            db.session.close()

    # @TODO:
    # Create a POST endpoint to get questions to play the quiz.
    # This endpoint should take category and previous question parameters
    # and return a random questions within the given category,
    # if provided, and that is not one of the previous questions.

    # TEST: In the "Play" tab, after a user selects "All" or a category,
    # one question at a time is displayed, the user is allowed to answer
    # and shown whether they were correct or not.
    @app.route('/quiz', methods=['POST'])
    def quiz():
        try:
            body = request.get_json()
            if body == None:
                questionsQuery = Question.query.all()
                return jsonify({'success': True, 'question': questionsQuery[random.randrange(len(questionsQuery))].format()})

            category = body.get('category', None)
            if category == None or category == 'all':
                questionsQuery = Question.query.filter(
                    Question.id != body.get('question_id', None)).all()
                return jsonify({'success': True, 'question': questionsQuery[random.randrange(len(questionsQuery))].format()})
        except:
            db.session.rollback()
            print(sys.exc_info())
            abort(500)
        finally:
            db.session.close()

      #   '''
      # @TODO:
      # Create error handlers for all expected errors
      # including 404 and 422.
      # '''

    return app
