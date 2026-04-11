from utils.exceptions import DuplicateEntryError, InvalidInputError


def validate_marks(marks):
    if marks <= 0:
        raise InvalidInputError("Marks must be greater than 0")


def validate_non_empty(value, field_name):
    if value is None or str(value).strip() == "":
        raise InvalidInputError(f"{field_name} cannot be empty")


def validate_int_range(value, min_value, max_value, field_name):
    if value < min_value or value > max_value:
        raise InvalidInputError(f"{field_name} must be between {min_value} and {max_value}")


def validate_menu_choice(choice, valid_choices):
    if choice not in valid_choices:
        valid = ", ".join(sorted(valid_choices))
        raise InvalidInputError(f"Invalid menu choice. Choose one of: {valid}")


def validate_unique_question(question_text, questions):
    normalized = question_text.strip().lower()
    for question in questions:
        if question["question"].strip().lower() == normalized:
            raise DuplicateEntryError("Duplicate question entry")