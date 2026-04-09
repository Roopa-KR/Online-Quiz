from flask import Flask, render_template, request, redirect, url_for, session
from services.auth_service import login, register, delete_user
from services.exam_service import create_exam, get_exams

app = Flask(__name__)
app.secret_key = "secret123"


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

    return render_template("dashboard.html", role=session["role"])


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


# 🚪 LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ▶️ RUN
if __name__ == "__main__":
    app.run(debug=True)