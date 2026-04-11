class Question:
    def __init__(self, question, options, correct_answer, question_id=None):
        self.question_id = question_id
        self.question = question
        self.options = options
        self.correct_answer = correct_answer

    def __str__(self):
        prefix = f"[{self.question_id}] " if self.question_id is not None else ""
        return f"{prefix}{self.question}"

    def __repr__(self):
        return f"Question(id={self.question_id}, question={self.question!r}, correct_answer={self.correct_answer})"

    def display(self):
        print("\n" + self.question)
        for i, option in enumerate(self.options, 1):
            print(f"{i}. {option}")

    def to_dict(self):
        return {
            "id": self.question_id,
            "question": self.question,
            "option1": self.options[0],
            "option2": self.options[1],
            "option3": self.options[2],
            "option4": self.options[3],
            "correct_answer": self.correct_answer,
        }

    @staticmethod
    def from_dict(data):
        return Question(
            data["question"],
            [data["option1"], data["option2"], data["option3"], data["option4"]],
            int(data["correct_answer"]),
            int(data["id"]) if data.get("id") else None,
        )