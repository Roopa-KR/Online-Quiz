from config.db_config import get_connection


GENERAL_KNOWLEDGE_QUESTIONS = [
	("Capital of India?", ["Delhi", "Mumbai", "Chennai", "Kolkata"], 1),
	("Which planet is known as the Red Planet?", ["Earth", "Mars", "Venus", "Jupiter"], 2),
	("How many continents are there?", ["Five", "Six", "Seven", "Eight"], 3),
	("What is the largest ocean on Earth?", ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"], 4),
	("Which animal is known as the ship of the desert?", ["Horse", "Camel", "Elephant", "Goat"], 2),
	("Which is the longest river in the world?", ["Amazon River", "Nile River", "Ganga River", "Yamuna River"], 2),
	("How many colors are there in a rainbow?", ["Five", "Six", "Seven", "Eight"], 3),
	("Which country is famous for the Eiffel Tower?", ["Italy", "France", "Germany", "Spain"], 2),
	("What is the currency of Japan?", ["Yuan", "Won", "Yen", "Ringgit"], 3),
	("Which gas do plants absorb from the air?", ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"], 3),
]

PYTHON_QUESTIONS = [
	("Which keyword is used to define a function in Python?", ["func", "def", "define", "lambda"], 2),
	("Which data type is immutable?", ["List", "Dictionary", "Set", "Tuple"], 4),
	("What does len([1, 2, 3]) return?", ["2", "3", "4", "Error"], 2),
	("Which symbol is used for comments in Python?", ["//", "#", "/*", "--"], 2),
	("Which of these is a Python loop?", ["repeat", "foreach", "for", "cycle"], 3),
	("What is the output type of input() in Python 3?", ["int", "float", "str", "bool"], 3),
	("Which method adds an item to the end of a list?", ["add()", "append()", "insert()", "push()"], 2),
	("Which operator is used for exponentiation?", ["^", "**", "%%", "//"], 2),
	("What does the break statement do?", ["Ends the program", "Stops the current loop", "Skips one iteration", "Creates a function"], 2),
	("Which collection stores key-value pairs?", ["List", "Tuple", "Set", "Dictionary"], 4),
]

SQL_QUESTIONS = [
	("Which SQL clause is used to filter rows?", ["ORDER BY", "GROUP BY", "WHERE", "HAVING"], 3),
	("Which command is used to remove all records but keep the table?", ["DROP", "TRUNCATE", "DELETE TABLE", "REMOVE"], 2),
	("Which SQL keyword is used to sort results?", ["SORT BY", "ORDER BY", "GROUP BY", "ARRANGE"], 2),
	("Which aggregate function returns the number of rows?", ["SUM", "COUNT", "AVG", "TOTAL"], 2),
	("Which statement is used to add new rows to a table?", ["ADD", "APPEND", "INSERT INTO", "CREATE"], 3),
	("Which join returns only matching rows from both tables?", ["LEFT JOIN", "RIGHT JOIN", "FULL JOIN", "INNER JOIN"], 4),
	("Which command modifies existing records in a table?", ["ALTER", "UPDATE", "MODIFY", "CHANGE"], 2),
	("Which SQL clause groups rows with the same values?", ["GROUP BY", "ORDER BY", "UNION", "DISTINCT"], 1),
	("What does DDL stand for?", ["Data Definition Language", "Data Deletion Language", "Database Development Logic", "Data Driver Layer"], 1),
	("Which clause is used to filter grouped data?", ["WHERE", "HAVING", "ORDER BY", "LIMIT"], 2),
]


def seed_exam(cursor, exam_name, questions):
	cursor.execute("SELECT id FROM exams WHERE name=?", (exam_name,))
	row = cursor.fetchone()

	if row is None:
		cursor.execute(
			"INSERT INTO exams (name, total_marks) VALUES (?, ?)",
			(exam_name, 10),
		)
		exam_id = cursor.lastrowid
	else:
		exam_id = row[0]
		cursor.execute(
			"UPDATE exams SET total_marks=? WHERE id=?",
			(10, exam_id),
		)

	cursor.execute("DELETE FROM questions WHERE exam_id=?", (exam_id,))

	for question, options, correct_answer in questions:
		cursor.execute(
			"""
			INSERT INTO questions
			(exam_id, question, option1, option2, option3, option4, correct_answer)
			VALUES (?, ?, ?, ?, ?, ?, ?)
			""",
			(exam_id, question, options[0], options[1], options[2], options[3], correct_answer),
		)


def main():
	conn = get_connection()
	cursor = conn.cursor()

	cursor.execute("DELETE FROM results WHERE exam_id IN (SELECT id FROM exams WHERE name = ?)", ("GK",))
	cursor.execute("DELETE FROM questions WHERE exam_id IN (SELECT id FROM exams WHERE name = ?)", ("GK",))
	cursor.execute("DELETE FROM exams WHERE name = ?", ("GK",))

	seed_exam(cursor, "General Knowledge", GENERAL_KNOWLEDGE_QUESTIONS)
	seed_exam(cursor, "Python", PYTHON_QUESTIONS)
	seed_exam(cursor, "SQL", SQL_QUESTIONS)

	conn.commit()
	conn.close()

	print("Quiz data seeded successfully.")


if __name__ == "__main__":
	main()