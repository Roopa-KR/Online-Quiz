import os
import sqlite3

def get_connection():
    db_path = os.getenv("DB_PATH", "exam.db")
    return sqlite3.connect(db_path)