class Exam:
    def __init__(self, name, total_marks):
        self.name = name
        self.total_marks = total_marks

    def __repr__(self):
        return f"Exam({self.name}, {self.total_marks})"