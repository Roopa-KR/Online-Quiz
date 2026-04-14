from datetime import datetime, timedelta

from config.db_config import get_connection


def _ensure_results_completion_column(cur):
    cur.execute("PRAGMA table_info(results)")
    columns = [row[1] for row in cur.fetchall()]
    if "completed_at" not in columns:
        cur.execute("ALTER TABLE results ADD COLUMN completed_at TEXT")

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
    _ensure_results_completion_column(cur)
    cur.execute(
        "INSERT INTO results (username, exam_id, score, completed_at) VALUES (?,?,?,CURRENT_TIMESTAMP)",
        (username, exam_id, score),
    )
    conn.commit()
    conn.close()


def _parse_timestamp(value):
    if not value:
        return None

    if isinstance(value, datetime):
        return value

    for format_string in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(value, format_string)
        except (TypeError, ValueError):
            continue

    try:
        return datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return None


def _calculate_current_streak(activity_dates):
    if not activity_dates:
        return 0

    streak = 0
    current_day = max(activity_dates)

    while current_day in activity_dates:
        streak += 1
        current_day -= timedelta(days=1)

    return streak


def get_user_score_summary(username):
    conn = get_connection()
    cur = conn.cursor()
    try:
        _ensure_results_completion_column(cur)
        cur.execute(
            """
            SELECT r.score, e.total_marks, r.completed_at
            FROM results r
            JOIN exams e ON e.id = r.exam_id
            WHERE r.username = ?
            ORDER BY r.completed_at DESC, r.id DESC
            """,
            (username,),
        )
        result_rows = cur.fetchall()

        cur.execute(
            "SELECT last_login_at FROM users WHERE username = ?",
            (username,),
        )
        user_row = cur.fetchone()

        if not result_rows and not user_row:
            return {
                "has_data": False,
                "average_score": None,
                "tests_passed": 0,
                "current_streak": 0,
            }

        percentages = []
        tests_passed = 0
        activity_dates = set()

        for score, total_marks, completed_at in result_rows:
            if total_marks and total_marks > 0:
                percentage = round((score / total_marks) * 100)
                percentages.append(percentage)
                if percentage >= 50:
                    tests_passed += 1

            parsed_completed_at = _parse_timestamp(completed_at)
            if parsed_completed_at:
                activity_dates.add(parsed_completed_at.date())

        if user_row and user_row[0]:
            parsed_login_at = _parse_timestamp(user_row[0])
            if parsed_login_at:
                activity_dates.add(parsed_login_at.date())

        average_score = round(sum(percentages) / len(percentages)) if percentages else None

        return {
            "has_data": bool(percentages or activity_dates),
            "average_score": average_score,
            "tests_passed": tests_passed,
            "current_streak": _calculate_current_streak(activity_dates),
        }
    finally:
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