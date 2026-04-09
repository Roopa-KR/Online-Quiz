from utils.exceptions import InvalidInputError

def validate_marks(marks):
    if marks <= 0:
        raise InvalidInputError("Marks must be greater than 0")