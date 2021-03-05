# Trivia API Backend

## Getting Started

### Installing Dependencies
To start up this project, please make sure that python is installed, as well as these dependencies:
- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework.
- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM will be used to handle the database interactions.
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension used to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the this directory run command:
```
flask run
```
You can also edit environmental variables in the `.env` file.
### Environmental Variable
Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.
Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Endpoints

Every endpoint has a `success` variable inside it's response that states if the request was processed successfully or not.
```json
{
  "success": true,
  "...": "..."
}
```

### GET '/categories':
- Request Arguments: None
- Returns: An object with a total count of categories, and the list of categories.
- Response:
```json
{
    "categories": {
      "1": "science",
      "2": "Art",
      "3": "History",
      "4": "Entertainment",
      "5": "Sports",
      "6": "Geography"
  },
  "total_categories": 6
}
```

### GET '/questions':
- Request Arguments: None
- Request Parameters: page(optional). ex: `http://127.0.0.1:5000/questions?page=2`
- Returns: An object with a total questions count, question list, and categories.
- Response:
```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "History",
        "4": "Entertainment",
        "5": "Sports",
        "6": "Geography"
    },
    "questions": [
      {
        "answer": "11 AM Wednesday",
        "category": 6,
        "difficulty": 2,
        "id": 1,
        "question": "When it's 9 PM in New York on Tuesday, what time is it in Echuca, Australia?"
      },
      {
        "answer": "What ancient people based their law on Hammurabi's Code?",
        "category": 1,
        "difficulty": 2,
        "id": 2,
        "question": "Mesopotamians"
      },
      {
        "answer": "Hudson",
        "category": 6,
        "difficulty": 2,
        "id": 1,
        "question": "What is the largest bay in the world?"
      }
    ],
    "total_questions": 6
}
```

### GET '/categories/(Category id)':
- Request Arguement: None
- Request Parameters: Category id in the url. ex: `http://127.0.0.1:5000/categories/2`
- Returns: An object with a category name, list of questions in category, and total_questions count
- Response:
```json
{
  "category": "science",
  "questions": [
      {
        "answer": "11 AM Wednesday",
        "category": 6,
        "difficulty": 2,
        "id": 1,
        "question": "When it's 9 PM in New York on Tuesday, what time is it in Echuca, Australia?"
      },
      {
        "answer": "Hudson",
        "category": 6,
        "difficulty": 2,
        "id": 1,
        "question": "What is the largest bay in the world?"
      }
    ],
  "total_questions": 2
}
```

### POST '/questions':
- Request Arguments: question, category, difficulty, answer. ex:
```json
{
  "question": "What game do the M.I.T. students play to win in the movie \"21\"?",
  "answer": "Blackjack",
  "difficulty": 3,
  "category": 4
}
```
- Returns An object with the total questions new count, and the new question added
- Response:
```json
{
    "question": {
        "answer": "Blackjack",
        "category": 4,
        "difficulty": 3,
        "id": 7,
        "question": "What game do the M.I.T. students play to win in the movie \"21\"?"
    },
    "total_questions": 7
}
```

### POST '/questions/search':
- Request Arguments: (searchTerm Number). ex:
```json
{
  "searchTerm": "what"
}
```
- Returns: An object with the found with the count of questions found total_matches, and list of questions
- Response:
```json
{
  "questions": [
    {
      "answer": "What ancient people based their law on Hammurabi's Code?",
      "category": 1,
      "difficulty": 2,
      "id": 2,
      "question": "Mesopotamians"
    },
    {
      "answer": "Hudson",
      "category": 6,
      "difficulty": 2,
      "id": 1,
      "question": "What is the largest bay in the world?"
    }
  ],
  "success": true,
  "total_matches": 2
  }
```

### POST '/quiz':
- Request Arguments: category(Integer-optional), previousQuestions(array of question ids-optional). ex:
```json
{
  "previousQuestions": [1,3,6,4,2,5],
  "category": 4
}
```
- Returns: A question randomly selected from the category and not from the previous question ids
- Response:
```json
{
  "question": {
    "answer": "Blackjack",
    "category": 4,
    "difficulty": 3,
    "id": 7,
    "question": "What game do the M.I.T. students play to win in the movie \"21\"?"
  },
  "success": true
}
```

### DELETE  '/questions/(question id)':
- Request Arguments: None
- Returns: An object with the new total_questions count after deletion
- Response:
```json
{
  "success": true,
  "total_questions": 6
}
```

## Error Handling
If a error occurs, and object would be sent with the info about the error. ex:
```json
{
  "success": false,
  "error": 404,
  "message": "Not found"
}
```

## Testing
To run the tests, run
```
python test_flaskr.py
```