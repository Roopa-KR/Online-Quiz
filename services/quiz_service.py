from models.question import Question
from utils.exceptions import InvalidChoiceError

# Using COLLECTIONS (list)
questions_list = []


def add_question():
    try:
        q = input("Enter question: ")

        options = []
        for i in range(4):
            opt = input(f"Enter option {i+1}: ")
            options.append(opt)

        correct = int(input("Enter correct option number (1-4): "))

        if correct < 1 or correct > 4:
            raise InvalidChoiceError("Choice must be between 1 and 4")

        question_obj = Question(q, options, correct)
        questions_list.append(question_obj)

        print("Question added successfully!")

    except Exception as e:
        print("Error:", e)


def start_quiz():
    if not questions_list:
        print("No questions available!")
        return

    score = 0

    for q in questions_list:
        try:
            q.display()
            answer = int(input("Enter your answer: "))

            if answer < 1 or answer > 4:
                raise InvalidChoiceError("Invalid option!")

            if answer == q.correct_answer:
                score += 1

        except Exception as e:
            print("Error:", e)

    print(f"\nYour Score: {score}/{len(questions_list)}")