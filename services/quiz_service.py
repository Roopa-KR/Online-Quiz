import csv
import os

from models.question import Question
from utils.exceptions import (
    DataPersistenceError,
    DuplicateEntryError,
    InvalidChoiceError,
    InvalidInputError,
    RecordNotFoundError,
)
from utils.validators import (
    validate_int_range,
    validate_non_empty,
    validate_unique_question,
)


DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
QUESTION_FILE = os.path.join(DATA_DIR, "questions.csv")
CSV_COLUMNS = ["id", "question", "option1", "option2", "option3", "option4", "correct_answer"]


# List collection for multiple records; each record is a dictionary.
questions_list = []


def ensure_data_store():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(QUESTION_FILE):
        with open(QUESTION_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_COLUMNS)
            writer.writeheader()


def load_questions_from_file():
    global questions_list
    ensure_data_store()

    try:
        with open(QUESTION_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            questions_list = []
            for row in reader:
                question = Question.from_dict(row)
                questions_list.append(question.to_dict())
    except OSError as error:
        raise DataPersistenceError("Failed to load questions from file") from error


def save_questions_to_file():
    ensure_data_store()
    try:
        with open(QUESTION_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_COLUMNS)
            writer.writeheader()
            for question in questions_list:
                writer.writerow(question)
    except OSError as error:
        raise DataPersistenceError("Failed to save questions to file") from error


def _next_question_id():
    if not questions_list:
        return 1
    return max(int(question["id"]) for question in questions_list) + 1


def _find_question_by_id(question_id):
    for question in questions_list:
        if int(question["id"]) == question_id:
            return question
    return None


def add_question():
    try:
        q_text = input("Enter question: ").strip()
        validate_non_empty(q_text, "Question")
        validate_unique_question(q_text, questions_list)

        options = []
        for index in range(4):
            option = input(f"Enter option {index + 1}: ").strip()
            validate_non_empty(option, f"Option {index + 1}")
            options.append(option)

        correct = int(input("Enter correct option number (1-4): "))
        validate_int_range(correct, 1, 4, "Correct option")

        question_obj = Question(q_text, options, correct, _next_question_id())
        questions_list.append(question_obj.to_dict())
        save_questions_to_file()

        print("Record Added Successfully")

    except ValueError:
        print("Invalid Input: Enter numeric values where required")
    except (InvalidInputError, DuplicateEntryError) as error:
        print(f"Invalid Input: {error}")
    except DataPersistenceError as error:
        print(f"Error: {error}")


def view_questions():
    if not questions_list:
        print("Record Not Found: No questions available")
        return

    print("\n===== QUESTION LIST =====")
    for question in questions_list:
        print(f"ID: {question['id']} | {question['question']}")


def search_questions():
    keyword = input("Enter keyword to search: ").strip().lower()
    if not keyword:
        print("Invalid Input: Keyword cannot be empty")
        return

    matches = [question for question in questions_list if keyword in question["question"].lower()]

    if not matches:
        print("Record Not Found")
        return

    print("\n===== SEARCH RESULTS =====")
    for question in matches:
        print(f"ID: {question['id']} | {question['question']}")


def update_question():
    try:
        question_id = int(input("Enter question ID to update: "))
        question = _find_question_by_id(question_id)

        if not question:
            raise RecordNotFoundError("Question not found")

        new_question = input("Enter updated question text: ").strip()
        validate_non_empty(new_question, "Question")
        question["question"] = new_question

        for index in range(1, 5):
            new_option = input(f"Enter updated option {index}: ").strip()
            validate_non_empty(new_option, f"Option {index}")
            question[f"option{index}"] = new_option

        new_correct = int(input("Enter updated correct option (1-4): "))
        validate_int_range(new_correct, 1, 4, "Correct option")
        question["correct_answer"] = new_correct

        save_questions_to_file()
        print("Record Updated Successfully")

    except ValueError:
        print("Invalid Input: ID and correct option must be numbers")
    except (InvalidInputError, RecordNotFoundError) as error:
        print(f"Invalid Input: {error}")
    except DataPersistenceError as error:
        print(f"Error: {error}")


def delete_question():
    try:
        question_id = int(input("Enter question ID to delete: "))
        question = _find_question_by_id(question_id)
        if not question:
            raise RecordNotFoundError("Question not found")

        questions_list.remove(question)
        save_questions_to_file()
        print("Record Deleted Successfully")

    except ValueError:
        print("Invalid Input: Question ID must be a number")
    except RecordNotFoundError as error:
        print(f"Record Not Found: {error}")
    except DataPersistenceError as error:
        print(f"Error: {error}")


def start_quiz():
    if not questions_list:
        print("Record Not Found: No questions available")
        return

    score = 0

    for question_dict in questions_list:
        question = Question.from_dict(question_dict)

        try:
            question.display()
            answer = int(input("Enter your answer (1-4): "))
            if answer < 1 or answer > 4:
                raise InvalidChoiceError("Invalid option")

            if answer == question.correct_answer:
                score += 1

        except ValueError:
            print("Invalid Input: Please enter a number between 1 and 4")
        except InvalidChoiceError as error:
            print(f"Invalid Input: {error}")

    print(f"\nYour Score: {score}/{len(questions_list)}")


def print_summary():
    total_questions = len(questions_list)
    print("\n===== SUMMARY REPORT =====")
    print(f"Total Questions: {total_questions}")
    print("Data Source: questions.csv")


def initialize_console_data():
    try:
        load_questions_from_file()
    except DataPersistenceError as error:
        print(f"Error: {error}")