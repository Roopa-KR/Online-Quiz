# Examination System

A Flask and SQLite based examination system with role-based access for admin and student workflows.

## Overview

This project provides:

- User registration and login
- Role-based dashboard (admin and student)
- Exam creation (admin)
- Question creation flow
- Exam listing and start page
- User deletion (admin)
- A simple terminal quiz mode

## Tech Stack

- Python 3.10+
- Flask
- SQLite
- HTML/CSS templates

## Project Layout

- `app.py`: Flask web application entry point
- `main.py`: Terminal based quiz runner
- `init_db.py`: Initializes database tables
- `insert_data.py`: Inserts sample question data
- `config/db_config.py`: SQLite connection helper
- `services/`: Business logic for auth, exam, and quiz
- `models/`: Data models
- `templates/`: Flask templates
- `static/`: CSS assets
- `database/schema.sql`: Database schema definition

## Getting Started

### 1. Clone and enter project

```bash
git clone <your-repo-url>
cd examination_system
```

### 2. Create and activate virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

The `requirements.txt` file is currently empty. Install Flask manually:

```bash
pip install flask
```

Optional: save installed package versions:

```bash
pip freeze > requirements.txt
```

### 4. Initialize database

```bash
python init_db.py
```

Alternative initializer:

```bash
python database/init_db.py
```

### 5. (Optional) Insert sample data

```bash
python insert_data.py
```

## Run the Application

### Web app

```bash
python app.py
```

Open:

- http://127.0.0.1:5000

### CLI app

```bash
python main.py
```

## Main Web Routes

- `/` Login
- `/register` Register
- `/dashboard` Dashboard
- `/create_exam` Create exam (admin only)
- `/add_question` Add question (admin only)
- `/start_exam` Start exam page
- `/delete_user` Delete user (admin only)
- `/logout` Logout

## Database Tables

- `users`
- `exams`
- `questions`
- `results`

## Notes and Current Limitations

- Passwords are stored in plain text (should be hashed in production).
- Flask secret key is hard-coded in source.
- The web `add_question` flow currently stores questions in an in-memory list from `quiz_service.py`, not directly into the database.
- `requirements.txt` should be maintained with exact dependencies.

## Troubleshooting

- If login fails unexpectedly, verify records in `exam.db` and ensure user exists.
- If database errors occur, delete `exam.db` and re-run `python init_db.py`.
- If PowerShell blocks script activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## License

Use and modify this project for learning and internal use.
