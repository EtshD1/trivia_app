import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = os.getenv("DB_TEST_NAME")
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            os.getenv("DB_USER"),
            os.getenv("DB_PASS"),
            'localhost:5432',
            self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # TODO
    # Write at least one test for each test for successful operation and for expected errors.
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_categories'] > 0)
        self.assertTrue(data['success'])

    def test_post_question(self):
        jsonData = {'question': 'testing',
                    'category': 1,
                    'difficulty': 10,
                    'answer': 'Test should work'}
        res = self.client().post('/questions', json=jsonData)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_questions'] > 0)

    def test_fail_post_question(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'] > 0)

    def test_delete_question(self):
        seek = self.client().get(f'/questions')
        prevData = json.loads(seek.data)
        id = prevData['questions'][0]['id']

        res = self.client().delete(f'/questions/{id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_questions'])

    def test_fail_delete_question(self):
        res = self.client().delete(f'/questions/100000000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_search(self):
        search_term = {'searchTerm': "testing"}
        res = self.client().post('/questions/search', json=search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_matches'])
        self.assertTrue(data['questions'])

    def test_fail_search(self):
        res = self.client().post('/questions/search')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_quiz(self):
        jsonData = {
            "previousQuestions": [1],
            "category": 1
        }
        res = self.client().post('/quiz', json=jsonData)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertNotEqual(data['question'], jsonData['previousQuestions'][0])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
