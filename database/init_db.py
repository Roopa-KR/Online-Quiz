import sqlite3

def init_db():
    conn = sqlite3.connect("exam.db")
    cursor = conn.cursor()

    with open("database/schema.sql", "r") as f:
        cursor.executescript(f.read())

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db() 