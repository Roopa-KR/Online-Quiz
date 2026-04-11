from service import (
    add_question,
    delete_question,
    initialize_console_data,
    print_summary,
    search_questions,
    start_quiz,
    update_question,
    view_questions,
)
from utils.exceptions import InvalidInputError
from utils.validators import validate_menu_choice

def menu():
    initialize_console_data()

    while True:
        print("\n===== EXAM SYSTEM (CONSOLE) =====")
        print("1. Add Record")
        print("2. View Records")
        print("3. Search Record")
        print("4. Update Record")
        print("5. Delete Record")
        print("6. Start Quiz")
        print("7. Summary Report")
        print("8. Exit")

        choice = input("Enter choice: ")

        try:
            validate_menu_choice(choice, {"1", "2", "3", "4", "5", "6", "7", "8"})

            if choice == "1":
                add_question()

            elif choice == "2":
                view_questions()

            elif choice == "3":
                search_questions()

            elif choice == "4":
                update_question()

            elif choice == "5":
                delete_question()

            elif choice == "6":
                start_quiz()

            elif choice == "7":
                print_summary()

            elif choice == "8":
                print("Exiting...")
                break

        except InvalidInputError as error:
            print(f"Invalid Input: {error}")
        except Exception as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    menu()