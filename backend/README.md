# Trivia API Backend

## Getting Started

### Installing Dependencies
To start up this project, please make sure that python is installed, as well as these dependencies:
- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework.
- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM will be used to handle the database interactions.
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension used to handle cross origin requests from our frontend server. 

## Database Setup
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

Every endpoint has a `success` variable inside that states if the request was processed successfully or not.

### GET '/categories':
- Request Arguments: None
- Returns: An object with a total_categories count, and a list of categories, that contains a object of id: category key:value pairs. 

### GET '/questions':
- Request Arguments: None
- Request Parameters: page(optional)
- Returns: An object with a total_questions count, question list, and categories.

### GET '/categories/(Category id)':
- Request Arguments: Category id in the url
- Returns: An object with a category name, list of questions in category, and total_questions count

### POST '/questions':
- Request Arguments: question, category, difficulty, answer
- Returns An object with the total_questions new count, and the new question added

### POST '/questions/search':
- Request Arguments: (search_term String)
- Returns: An object with the found with the count of questions found total_matches, and list of questions

### POST '/quiz':
- Request Arguments: category(Integer-optional), previousQuestions(array of question ids-optional)
- Returns: A question randomly selected from the category and not from the previous question ids

### DELETE  '/questions/(question id)':
- Request Arguments: None
- Returns: An object with the new total_questions count after deletion

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