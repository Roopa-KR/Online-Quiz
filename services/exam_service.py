from config.db_config import get_connection

def create_exam(name, marks):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO exams VALUES (NULL,?,?)", (name, marks))
    conn.commit()
    conn.close()

def get_exams():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM exams")
    data = cur.fetchall()
    conn.close()
    return data


def get_exam_by_id(exam_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM exams WHERE id=?", (exam_id,))
    data = cur.fetchone()
    conn.close()
    return data

def get_questions(exam_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM questions WHERE exam_id=?", (exam_id,))
    data = cur.fetchall()
    conn.close()
    return data

def save_result(username, exam_id, score):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO results VALUES (NULL,?,?,?)",
                (username, exam_id, score))
    conn.commit()
    conn.close()

def get_leaderboard():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT username, SUM(score) 
        FROM results 
        GROUP BY username 
        ORDER BY SUM(score) DESC
    """)
    data = cur.fetchall()
    conn.close()
    return data

def get_attended_tests(username):
    """Get all tests attended by a specific user"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT r.exam_id, e.name, e.total_marks, r.score
        FROM results r
        JOIN exams e ON r.exam_id = e.id
        WHERE r.username = ?
        ORDER BY r.id DESC
    """, (username,))
    data = cur.fetchall()
    conn.close()
    return data