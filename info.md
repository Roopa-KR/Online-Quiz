# Examination System - Full Code Explanation

## What this project is
This project is an examination management system built with Python, Flask, SQLite, HTML templates, and CSS. It has two main parts:

1. A web application for login, registration, dashboard, exams, question management, and results.
2. A console-based quiz application for adding, viewing, searching, updating, deleting, and attempting questions from a CSV file.

The project is split into small modules so that database logic, validation, models, and application routes stay organized.

---

## High-level architecture

### Main layers
- `app.py` - Flask web app entry point.
- `main.py` - console menu entry point.
- `services/` - business logic and database operations.
- `models/` - object-oriented data classes.
- `utils/` - validation and custom exceptions.
- `config/db_config.py` - database connection helper.
- `templates/` - HTML pages for the web UI.
- `static/style.css` - styling for the web UI.
- `init_db.py` - database table creation.
- `insert_data.py` - inserts sample web data.
- `database/init_db.py` - alternative schema initializer from `database/schema.sql`.
- `database/schema.sql` - SQL schema file.

### Data storage used by the project
- SQLite database file: `exam.db` by default.
- CSV file: `data/questions.csv` for the console quiz module.

---

## How the application connects to the database

### `config/db_config.py`
This file contains the database connection helper:

- It reads `DB_PATH` from the environment.
- If `DB_PATH` is not set, it uses `exam.db`.
- It returns a SQLite connection using `sqlite3.connect(db_path)`.

This is the central place where database access starts. All services that need the database import `get_connection()` from here.

### Why this matters
This avoids repeating connection code in multiple files and keeps the database path configurable.

---

## Database initialization

### `init_db.py`
This script creates the tables used by the Flask app:

- `users`
- `exams`
- `questions`
- `results`

It also handles older databases by checking whether these columns exist:
- `users.last_login_at`
- `results.completed_at`

If the column is missing, it runs `ALTER TABLE` to add it.

### `database/init_db.py`
This is a second initializer that loads schema from `database/schema.sql` and creates the database structure from that file.

### Why there are two initializers
The project appears to support two setup styles:
- direct Python table creation in `init_db.py`
- SQL-file based setup in `database/init_db.py`

In practice, `init_db.py` is the more complete initializer for the current codebase because it also includes compatibility checks for older databases.

---

## Flask web application flow

### `app.py`
This is the main web application.

#### What it does
- Creates the Flask app.
- Loads environment variables using `dotenv`.
- Sets the secret key.
- Defines routes for login, registration, dashboard, exam creation, question management, quiz taking, and user deletion.
- Injects score summary data into templates using a context processor.

### Important imports
- `Flask`, `render_template`, `request`, `redirect`, `url_for`, `session` from Flask.
- Authentication functions from `services/auth_service.py`.
- Exam functions from `services/exam_service.py`.

### `@app.context_processor`
This is important for the score modal.

It injects `score_summary` into all templates automatically. That means the modal in `base.html` can use:
- `score_summary.average_score`
- `score_summary.tests_passed`
- `score_summary.current_streak`

without each route passing them manually.

### Login route `/`
- On GET, it shows the login page.
- On POST, it reads `username` and `password`.
- It calls `login(username, password)` from `auth_service`.
- If login succeeds, it stores user data in `session` and redirects to the dashboard.
- If login fails, it re-renders the login page with the error message:
  `Wrong password, please try again`
  and preserves the entered username.

This is backend validation because the server checks whether the credentials are valid.

### Register route `/register`
- On POST, it reads username, password, and role.
- It calls `register()` in `auth_service`.
- If registration succeeds, it redirects to login.
- If the user already exists, it returns a message.

### Dashboard route `/dashboard`
- Requires a logged-in user.
- Loads exams from the database.
- Renders the dashboard with the current role and the list of exams.

### Test history route `/test_history`
- Requires login.
- Loads attended tests for the current user.
- Renders the history page.

### Create exam route `/create_exam`
- Admin only.
- On POST, creates a new exam.
- Redirects to add questions.

### Add question route `/add_question`
- Admin only.
- Uses the in-memory `questions_list` from `services/quiz_service.py`.
- Converts form input into a `Question` object.
- Appends it to the list.

### Start exam routes
- `/start_exam` lists exams.
- `/start_exam/<int:exam_id>` shows questions for one exam and processes submitted answers.
- On submission, it calculates score, stores the result, creates review data, and shows a review page.

### Delete user route `/delete_user`
- Admin only.
- Deletes a user by username.
- Prevents the admin from deleting their own account.

---

## Authentication and user database logic

### `services/auth_service.py`
This file handles user-related database operations.

#### `_ensure_users_login_column(cur)`
This helper checks whether `last_login_at` exists in the `users` table.
If not, it adds the column.

#### `register(username, password, role)`
- Ensures the login column exists.
- Inserts a new user into the `users` table.
- Stores `last_login_at` as `NULL` initially.
- Returns `True` if successful.
- Returns `False` if an error occurs.

#### `login(username, password)`
- Ensures the login column exists.
- Selects a user with matching username and password.
- If no match is found, returns `None`.
- If a user is found, it updates `last_login_at` to the current timestamp.
- Then it fetches the updated row and returns it.

This is the main backend validation for login. The web app uses the result to decide whether to redirect or show the error message.

#### `delete_user(username)`
- Finds the user.
- Raises an error if the user does not exist.
- Deletes the user if found.

### Important note
Passwords are stored in plain text. That is acceptable for a learning project, but in a real system passwords should be hashed.

---

## Exam database logic and score summary

### `services/exam_service.py`
This file contains database logic for exams, questions, results, and score calculations.

#### `_ensure_results_completion_column(cur)`
Checks whether `results.completed_at` exists.
If not, adds it.

#### `create_exam(name, marks)`
Inserts a new exam into `exams`.

#### `get_exams()`
Returns all exams.

#### `get_exam_by_id(exam_id)`
Returns a single exam row.

#### `get_questions(exam_id)`
Returns all questions for a particular exam.

#### `save_result(username, exam_id, score)`
- Ensures `completed_at` exists.
- Inserts the result with `CURRENT_TIMESTAMP`.
- This timestamp is later used for user streak calculations.

#### `get_attended_tests(username)`
Returns the user's test history by joining `results` and `exams`.

#### `get_user_score_summary(username)`
This powers the score modal.

It calculates:
- `average_score` - average percentage across all tests.
- `tests_passed` - count of tests where percentage is at least 50.
- `current_streak` - consecutive active days using test completion dates and the last login date.

It also returns:
- `has_data` - `True` if the user has any results or activity.

### How streak is calculated
The code collects activity dates from:
- `results.completed_at`
- `users.last_login_at`

Then it starts from the most recent date and counts backward day by day until the chain breaks.

### Edge cases handled
- No test history and no login activity: returns no data.
- Missing timestamps: ignored safely.
- Existing databases without the new columns: migration helper adds them.

---

## Console quiz application

### `main.py`
This is the CLI entry point.

#### Flow
- Calls `initialize_console_data()` at startup.
- Shows a text menu.
- Validates the menu choice using `validate_menu_choice()`.
- Calls the matching operation:
  - add question
  - view questions
  - search questions
  - update question
  - delete question
  - start quiz
  - summary report

### Why this is useful
It gives a terminal-based version of the quiz system for simple testing and question management.

---

## Console service logic and CSV storage

### `service.py`
This file handles question management in the console app.

#### Data storage
- Uses `data/questions.csv`
- Keeps an in-memory list called `questions_list`

#### `ensure_data_store()`
- Creates the data directory if needed.
- Creates the CSV file with headers if it does not exist.

#### `load_questions_from_file()`
- Reads CSV records.
- Converts each row to a `Question` object using `Question.from_dict()`.
- Stores them in `questions_list`.

#### `save_questions_to_file()`
- Writes the current list back to CSV.

#### `_next_question_id()`
Returns the next available question ID.

#### `_find_question_by_id(question_id)`
Searches the list for a matching question.

#### `add_question()`
- Prompts the user for question text, options, and correct answer.
- Uses validation helpers.
- Prevents duplicate questions.
- Creates a `Question` object.
- Saves it to the CSV.

#### `view_questions()`
Prints all questions.

#### `search_questions()`
Searches question text by keyword.

#### `update_question()`
- Finds a question by ID.
- Lets the user change text, options, and correct answer.
- Saves changes to CSV.

#### `delete_question()`
Removes a question from the list and saves the file.

#### `start_quiz()`
- Iterates through the loaded questions.
- Shows each question.
- Reads the answer from the user.
- Compares it to the correct answer.
- Increments score when correct.

#### `print_summary()`
Prints total questions and data source.

#### `initialize_console_data()`
Loads the CSV file when the console app starts.

### How validation is used here
This file uses validation heavily before adding or updating data.

Examples:
- `validate_non_empty()` for question text and options.
- `validate_unique_question()` to prevent duplicates.
- `validate_int_range()` to ensure correct answer is between 1 and 4.
- `InvalidChoiceError` when a quiz answer is outside the valid range.

---

## Validation layer

### `utils/validators.py`
This file holds reusable validation functions.

#### `validate_marks(marks)`
Ensures marks are greater than 0.

#### `validate_non_empty(value, field_name)`
Ensures a field is not blank.

#### `validate_int_range(value, min_value, max_value, field_name)`
Ensures a numeric value falls within a valid range.

#### `validate_menu_choice(choice, valid_choices)`
Ensures console menu input is one of the allowed values.

#### `validate_unique_question(question_text, questions)`
Ensures a question is not duplicated in the question list.

### Where validation is used
- Console app menu selection.
- Adding or updating questions.
- Quiz answer checking.
- Registration and login route validation is mostly handled through the database/service logic and form required fields.

### Backend vs frontend validation
- Frontend validation: HTML `required` fields and preserved input values.
- Backend validation: service functions, validator helpers, and login checks.

The login error message is a good example of backend validation feeding the frontend display.

---

## Custom exceptions

### `utils/exceptions.py`
These are custom exception classes used to make error handling clearer:

- `InvalidChoiceError`
- `InvalidInputError`
- `DuplicateEntryError`
- `RecordNotFoundError`
- `DataPersistenceError`

### Why custom exceptions are useful
Instead of using only generic `Exception`, the code can raise precise errors and handle them more cleanly.

Examples:
- duplicate questions
- missing records
- invalid numeric input
- file read/write problems

---

## OOP in this project

The project uses object-oriented programming in the `models/` package.

### `models/user.py`
```python
class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role

    def __str__(self):
        return f"{self.username} ({self.role})"
```

#### What it represents
A simple user object with username and role.

#### OOP concepts used
- Class
- Object
- Attributes
- Constructor

### `models/exam.py`
```python
class Exam:
    def __init__(self, name, total_marks):
        self.name = name
        self.total_marks = total_marks

    def __repr__(self):
        return f"Exam({self.name}, {self.total_marks})"
```

#### What it represents
An exam object with name and total marks.

### `models/question.py`
This is the richest model in the project.

#### Attributes
- `question_id`
- `question`
- `options`
- `correct_answer`

#### Methods
- `__str__()`
- `__repr__()`
- `display()`
- `to_dict()`
- `from_dict()`

#### What each method does
- `__str__()` gives a readable string when printing the object.
- `__repr__()` gives a debug-friendly representation.
- `display()` prints the question and options in the console.
- `to_dict()` converts the object into a dictionary for CSV storage.
- `from_dict()` creates a `Question` object from dictionary data.

### `model.py`
This is a convenience module that re-exports:
- `Exam`
- `Question`
- `User`

So other code can import them from one place if needed.

---

## Magic methods used in the project

Magic methods are special Python methods with double underscores.

### `__init__`
Used in all model classes.
It runs when an object is created and sets up the initial data.

### `__str__`
Used in:
- `User`
- `Question`

It controls how objects look when converted to strings or printed.

Example:
- `User("nisha", "student")` becomes `nisha (student)`

### `__repr__`
Used in:
- `Exam`
- `Question`

It provides a developer-friendly representation for debugging.

Example:
- `Exam(Math, 100)`
- `Question(id=1, question='Capital of India?', correct_answer=1)`

### Why magic methods matter here
They make debugging and object display easier, especially in the console quiz and when working with model objects.

---

## How the web UI works

### Templates
The web interface is built with Jinja2 templates in `templates/`.

Important pages:
- `login.html`
- `register.html`
- `dashboard.html`
- `create_exam.html`
- `add_question.html`
- `take_exam.html`
- `quiz.html`
- `review.html`
- `leaderboard.html`
- `test_history.html`
- `base.html`

### `templates/base.html`
This is the shared layout for the authenticated pages.
It contains:
- sidebar navigation
- top bar
- profile modal
- score modal
- notifications modal
- shared JavaScript for modals and sidebar behavior

### Dynamic score modal
The score modal uses `score_summary` from Flask context injection.
That makes it user-specific and dynamic instead of hardcoded.

### Frontend validation and UX
Examples:
- `required` inputs in forms
- error message blocks for login
- preserved username value on failed login
- scroll locking while modals are open

### `static/style.css`
This file styles the entire application.
It contains:
- login page layout
- dashboard layout
- card styles
- modal styling
- responsive behavior
- error message styling
- scroll lock styling for modals

---

## Data flow from login to dashboard

1. User submits login form.
2. `app.py` receives the POST request.
3. `auth_service.login()` checks the database.
4. If credentials are valid:
   - session values are set
   - user is redirected to the dashboard
5. If credentials are invalid:
   - login page is rendered again
   - error message is shown
   - username is preserved

---

## Data flow when taking an exam

1. User opens exam list.
2. User starts an exam.
3. Questions are loaded from the database.
4. User submits answers.
5. The app compares answers and calculates score.
6. `save_result()` stores the score in `results`.
7. The review page shows score and feedback quote.
8. The score summary on the dashboard/modal can update based on the new result.

---

## Validation summary

### Backend validation
- Login success/failure checking.
- Admin-only route access.
- Correct option range checking.
- Duplicate question protection.
- File/DB operation error handling.

### Frontend validation
- Required fields in forms.
- Error display in login UI.
- Preserved username value after failure.

### Console validation
- Menu input validation.
- Empty input validation.
- Numeric range validation.
- Duplicate question validation.

---

## Important limitations and notes

- Passwords are not hashed.
- The console quiz uses CSV storage, while the web app uses SQLite.
- Some data exists in the database, some in memory, and some in CSV, so the project has mixed storage strategies.
- The `add_question` flow in the web app currently uses an in-memory list in `quiz_service.py`, not direct database persistence.
- The score streak logic is based on login and test dates, so it is a practical approximation of user activity.

---

## Short summary

This project is a hybrid exam system:
- Flask handles the web UI.
- SQLite stores users, exams, questions, and results.
- CSV stores console quiz questions.
- Validation is implemented with helper functions and route checks.
- OOP is used through the model classes.
- Magic methods help represent objects cleanly.
- The login and score modal were made dynamic by passing backend data into templates.

If you read the code file by file in this order, the project becomes easy to understand:
1. `config/db_config.py`
2. `utils/validators.py` and `utils/exceptions.py`
3. `models/`
4. `services/`
5. `app.py`
6. `templates/`
7. `main.py` and `service.py`
