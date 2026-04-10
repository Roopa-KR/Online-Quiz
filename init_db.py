from config.db_config import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT,
    last_login_at TEXT
);

CREATE TABLE IF NOT EXISTS exams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    total_marks INTEGER
);

CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exam_id INTEGER,
    question TEXT,
    option1 TEXT,
    option2 TEXT,
    option3 TEXT,
    option4 TEXT,
    correct_answer INTEGER
);

CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    exam_id INTEGER,
    score INTEGER
);
""")

# Ensure older databases also get the login timestamp column.
cursor.execute("PRAGMA table_info(users)")
existing_columns = [row[1] for row in cursor.fetchall()]
if "last_login_at" not in existing_columns:
    cursor.execute("ALTER TABLE users ADD COLUMN last_login_at TEXT")

conn.commit()
conn.close()

print("Database & Tables Created Successfully!")