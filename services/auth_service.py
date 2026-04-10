from config.db_config import get_connection


def _ensure_users_login_column(cur):
    cur.execute("PRAGMA table_info(users)")
    columns = [row[1] for row in cur.fetchall()]
    if "last_login_at" not in columns:
        cur.execute("ALTER TABLE users ADD COLUMN last_login_at TEXT")


def register(username, password, role):
    conn = get_connection()
    cur = conn.cursor()
    try:
        _ensure_users_login_column(cur)
        cur.execute(
            "INSERT INTO users (username, password, role, last_login_at) VALUES (?,?,?,NULL)",
            (username, password, role),
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


def login(username, password):
    conn = get_connection()
    cur = conn.cursor()
    try:
        _ensure_users_login_column(cur)
        cur.execute(
            "SELECT id, username, password, role, last_login_at FROM users WHERE username=? AND password=?",
            (username, password),
        )
        user = cur.fetchone()

        if not user:
            return None

        cur.execute(
            "UPDATE users SET last_login_at = CURRENT_TIMESTAMP WHERE id=?",
            (user[0],),
        )
        conn.commit()

        cur.execute(
            "SELECT id, username, password, role, last_login_at FROM users WHERE id=?",
            (user[0],),
        )
        return cur.fetchone()
    finally:
        conn.close()


def delete_user(username):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()

        if not user:
            raise Exception("User not found")

        cursor.execute("DELETE FROM users WHERE username=?", (username,))
        conn.commit()

        print("User deleted successfully")

    except Exception as e:
        print("Error:", e)

    finally:
        conn.close()
