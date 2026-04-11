import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session
from services.auth_service import login, register, delete_user
from services.exam_service import create_exam, get_exams, get_exam_by_id, get_questions, save_result, get_attended_tests

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "secret123")


def format_member_since(timestamp):
    if not timestamp:
        return "Not available"

    try:
        parsed = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        return parsed.strftime("%d %b %Y, %I:%M %p")
    except ValueError:
        return str(timestamp)


def get_motivational_quote(score, total):
    if total == 0:
        return "Great start. Keep practicing and aim higher in your next exam."

    percentage = (score / total) * 100

    if percentage >= 80:
        return "Excellent effort. Keep the momentum going for the next challenge."
    if percentage >= 50:
        return "Good progress. Review your mistakes and you'll do even better next time."

    return "Do your best in the next exam. Every attempt makes you stronger."


# 🔐 LOGIN
@app.route("/", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = login(username, password)

        if user:
            session["user"] = user[1]
            session["role"] = user[3]
            session["member_since"] = format_member_since(user[4])
            return redirect(url_for("dashboard"))
        else:
            return "Login Failed"

    return render_template("login.html")


# 📝 REGISTER
@app.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        if register(username, password, role):
            return redirect(url_for("login_page"))
        else:
            return "User already exists"

    return render_template("register.html")


# 📊 DASHBOARD
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    exams = get_exams()
    return render_template("dashboard.html", role=session["role"], exams=exams)


# 📜 TEST HISTORY
@app.route("/test_history")
def test_history():
    if "user" not in session:
        return redirect("/")

    attended_tests = get_attended_tests(session["user"])
    return render_template("test_history.html", attended_tests=attended_tests)


# 🧠 CREATE EXAM (Admin only)
@app.route("/create_exam", methods=["GET", "POST"])
def create_exam_page():
    if "user" not in session:
        return redirect("/")

    if session.get("role") != "admin":
        return "Access Denied"

    if request.method == "POST":
        name = request.form["name"]
        marks = int(request.form["marks"])
        create_exam(name, marks)

        # ✅ Redirect to Add Question page
        return redirect(url_for("add_question_page"))

    return render_template("create_exam.html")


# ➕ ADD QUESTION (Admin only)
@app.route("/add_question", methods=["GET", "POST"])
def add_question_page():
    if "user" not in session:
        return redirect("/")

    if session.get("role") != "admin":
        return "Access Denied"

    from services.quiz_service import questions_list
    from models.question import Question

    if request.method == "POST":
        try:
            question = request.form["question"]
            option1 = request.form["option1"]
            option2 = request.form["option2"]
            option3 = request.form["option3"]
            option4 = request.form["option4"]
            correct = int(request.form["correct"])

            if correct < 1 or correct > 4:
                return "Invalid correct option (must be 1-4)"

            q = Question(
                question,
                [option1, option2, option3, option4],
                correct
            )

            questions_list.append(q)

            return "Question Added Successfully"

        except Exception as e:
            return f"Error: {e}"

    return render_template("add_question.html")


# 📚 START EXAM (Student/Admin)
@app.route("/start_exam")
def start_exam():
    if "user" not in session:
        return redirect("/")

    try:
        exams = get_exams()
        return render_template("take_exam.html", exams=exams)
    except Exception as e:
        return f"Error: {e}"


@app.route("/start_exam/<int:exam_id>", methods=["GET", "POST"])
def take_exam(exam_id):
    if "user" not in session:
        return redirect("/")

    try:
        exam = get_exam_by_id(exam_id)
        if not exam:
            return "Exam not found", 404

        questions = get_questions(exam_id)

        if request.method == "POST":
            score = 0
            review_data = []

            for question in questions:
                answer = request.form.get(str(question[0]))
                user_answer = int(answer) if answer is not None else None
                correct_answer = question[7]

                if user_answer == correct_answer:
                    score += 1

                review_data.append(
                    {
                        "question": question[2],
                        "options": [question[3], question[4], question[5], question[6]],
                        "user_answer": user_answer,
                        "correct_answer": correct_answer,
                        "is_correct": user_answer == correct_answer,
                    }
                )

            save_result(session["user"], exam_id, score)
            quote = get_motivational_quote(score, len(questions))
            return render_template(
                "review.html",
                score=score,
                total=len(questions),
                exam_name=exam[1],
                quote=quote,
                review_data=review_data,
            )

        return render_template("quiz.html", questions=questions, exam_name=exam[1])
    except Exception as e:
        return f"Error: {e}"


# 🗑️ DELETE USER (Admin only)
@app.route("/delete_user", methods=["GET", "POST"])
def delete_user_page():
    if "user" not in session:
        return redirect("/")

    if session.get("role") != "admin":
        return "Access Denied"

    if request.method == "POST":
        username = request.form["username"]

        if username == session.get("user"):
            return "You cannot delete your own account"

        delete_user(username)
        return "User Deleted Successfully"

    return render_template("delete_user.html")


# � API - GET ATTENDED TESTS
# �🚪 LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ▶️ RUN
if __name__ == "__main__":
    app.run(debug=True)