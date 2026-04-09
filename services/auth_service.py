from config.db_config import get_connection

def register(username, password, role):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users VALUES (NULL,?,?,?)",
                    (username, password, role))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login(username, password):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE username=? AND password=?",
                (username, password))
    user = cur.fetchone()
    conn.close()
    return user
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
