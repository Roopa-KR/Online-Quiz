from config.db_config import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT * FROM exams")
print(cursor.fetchall())

conn.close()