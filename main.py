from services.quiz_service import add_question, start_quiz
from services.auth_service import delete_user

def menu():
    while True:
        print("\n===== EXAM SYSTEM =====")
        print("1. Add Question (Admin)")
        print("2. Start Quiz (Student)")
        print("3. Exit")
        print("4. Delete User")

        choice = input("Enter choice: ")

        try:
            if choice == "1":
                add_question()

            elif choice == "2":
                start_quiz()

            elif choice == "3":
                print("Exiting...")
                break
            elif choice == "4":
                 username = input("Enter username to delete: ")
                 delete_user(username)

            else:
                raise ValueError("Invalid Menu Choice")

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    menu()