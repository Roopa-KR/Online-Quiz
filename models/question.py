class Question:
    def __init__(self, question, options, correct_answer):
        self.question = question
        self.options = options   # list
        self.correct_answer = correct_answer

    def __str__(self):
        return f"{self.question}"

    def display(self):
        print("\n" + self.question)
        for i, option in enumerate(self.options, 1):
            print(f"{i}. {option}")