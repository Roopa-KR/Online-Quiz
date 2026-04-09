from config.db_config import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
INSERT INTO questions 
(exam_id, question, option1, option2, option3, option4, correct_answer)
VALUES 
(1,'Capital of India?','Delhi','Mumbai','Chennai','Kolkata',1)
""")

conn.commit()
conn.close()

print("Question inserted successfully!")