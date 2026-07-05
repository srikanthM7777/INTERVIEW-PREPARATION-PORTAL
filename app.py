import os
import random
import time
from functools import wraps

from flask import (Flask, render_template, request, redirect, url_for,
                    session, flash, abort)
from werkzeug.utils import secure_filename

from config import Config
from models import (db, User, Question, CodingProblem, InterviewQuestion,
                     MockTest, Feedback)

app = Flask(__name__)
app.config.from_object(Config)

if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite:///"):
    db_path = app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", "")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

db.init_app(app)


# ---------------------------------------------------------------- helpers --
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("is_admin"):
            flash("Admin access required.", "danger")
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return wrapper


def current_user():
    uid = session.get("user_id")
    return User.query.get(uid) if uid else None


@app.context_processor
def inject_user():
    return {"current_user": current_user()}


# ------------------------------------------------------------------ home --
@app.route("/")
def index():
    return render_template("index.html")


# ------------------------------------------------------------ auth views --
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        college = request.form.get("college", "").strip()
        branch = request.form.get("branch", "").strip()
        year = request.form.get("year", "").strip()

        if not name or not email or not password:
            flash("Name, email and password are required.", "danger")
            return redirect(url_for("register"))

        if User.query.filter_by(email=email).first():
            flash("An account with this email already exists.", "danger")
            return redirect(url_for("register"))

        user = User(name=name, email=email, college=college, branch=branch, year=year)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session["user_id"] = user.id
            session["is_admin"] = user.is_admin
            flash(f"Welcome back, {user.name}!", "success")
            return redirect(url_for("dashboard"))

        flash("Invalid email or password.", "danger")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        new_password = request.form.get("new_password", "")
        user = User.query.filter_by(email=email).first()
        if user and new_password:
            user.set_password(new_password)
            db.session.commit()
            flash("Password updated. Please log in.", "success")
            return redirect(url_for("login"))
        flash("Email not found.", "danger")
    return render_template("forgot_password.html")


@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        user = current_user()
        old = request.form.get("old_password", "")
        new = request.form.get("new_password", "")
        if not user.check_password(old):
            flash("Current password is incorrect.", "danger")
        else:
            user.set_password(new)
            db.session.commit()
            flash("Password changed successfully.", "success")
            return redirect(url_for("profile"))
    return render_template("change_password.html")


# ------------------------------------------------------------- dashboard --
@app.route("/dashboard")
@login_required
def dashboard():
    user = current_user()
    tests = MockTest.query.filter_by(user_id=user.id).order_by(MockTest.date.desc()).limit(5).all()
    best_scores = {
        "aptitude": random.choice([None, 70, 85]),  # placeholder progress indicators
    }
    total_questions = Question.query.count()
    total_coding = CodingProblem.query.count()
    return render_template("dashboard.html", user=user, tests=tests,
                            total_questions=total_questions, total_coding=total_coding)


# -------------------------------------------------------------- aptitude --
APTITUDE_CATEGORIES = ["Quantitative", "Logical Reasoning", "Verbal", "Data Interpretation", "General Aptitude"]


@app.route("/aptitude")
@login_required
def aptitude():
    return render_template("aptitude.html", categories=APTITUDE_CATEGORIES)


@app.route("/aptitude/<category>")
@login_required
def aptitude_quiz(category):
    questions = Question.query.filter_by(section="aptitude", category=category).all()
    return render_template("quiz.html", questions=questions, category=category,
                            quiz_type="aptitude", back_url=url_for("aptitude"))


# ----------------------------------------------------------------- coding --
@app.route("/coding")
@login_required
def coding():
    difficulty = request.args.get("difficulty")
    language = request.args.get("language")
    query = CodingProblem.query
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    if language:
        query = query.filter_by(language=language)
    problems = query.all()
    languages = ["Python", "Java", "C", "C++", "JavaScript"]
    return render_template("coding.html", problems=problems, languages=languages,
                            selected_language=language, selected_difficulty=difficulty)


@app.route("/coding/<int:problem_id>")
@login_required
def coding_detail(problem_id):
    problem = CodingProblem.query.get_or_404(problem_id)
    return render_template("coding_detail.html", problem=problem)


# -------------------------------------------------------------- hr / tech --
@app.route("/hr")
@login_required
def hr():
    category = request.args.get("category")
    query = InterviewQuestion.query
    if category:
        query = query.filter_by(category=category)
    questions = query.all()
    categories = [c[0] for c in db.session.query(InterviewQuestion.category).distinct()]
    return render_template("interview.html", questions=questions, categories=categories,
                            selected_category=category)


TECHNICAL_SUBJECTS = ["DBMS", "Operating System", "Networking", "Python", "Java", "HTML", "CSS", "JavaScript", "SQL"]


@app.route("/technical")
@login_required
def technical():
    return render_template("technical.html", subjects=TECHNICAL_SUBJECTS)


@app.route("/technical/<subject>")
@login_required
def technical_quiz(subject):
    questions = Question.query.filter_by(section="technical", category=subject).all()
    return render_template("quiz.html", questions=questions, category=subject,
                            quiz_type="technical", back_url=url_for("technical"))


@app.route("/submit-quiz", methods=["POST"])
@login_required
def submit_quiz():
    total = int(request.form.get("total_questions", 0))
    score = 0
    for i in range(total):
        qid = request.form.get(f"qid_{i}")
        selected = request.form.get(f"answer_{i}")
        if qid and selected:
            q = Question.query.get(int(qid))
            if q and q.answer == selected:
                score += 1
    return render_template("result.html", score=score, total=total)


# -------------------------------------------------------------- mock test --
@app.route("/mock-test")
@login_required
def mock_test_intro():
    return render_template("mock_test.html")


@app.route("/mock-test/start")
@login_required
def mock_test_start():
    all_questions = Question.query.all()
    count = min(30, len(all_questions))
    questions = random.sample(all_questions, count) if all_questions else []
    return render_template("quiz.html", questions=questions, category="Mock Test",
                            quiz_type="mock", back_url=url_for("mock_test_intro"),
                            time_limit=1800, start_time=int(time.time()))


@app.route("/submit-mock-test", methods=["POST"])
@login_required
def submit_mock_test():
    total = int(request.form.get("total_questions", 0))
    start_time = int(request.form.get("start_time", int(time.time())))
    score = 0
    for i in range(total):
        qid = request.form.get(f"qid_{i}")
        selected = request.form.get(f"answer_{i}")
        if qid and selected:
            q = Question.query.get(int(qid))
            if q and q.answer == selected:
                score += 1

    time_taken = int(time.time()) - start_time
    test = MockTest(user_id=session["user_id"], score=score, total=total, time_taken=time_taken)
    db.session.add(test)
    db.session.commit()
    return render_template("result.html", score=score, total=total, mock=True, time_taken=time_taken)


# -------------------------------------------------------------- leaderboard
@app.route("/leaderboard")
@login_required
def leaderboard():
    results = (
        db.session.query(User, db.func.max(MockTest.score).label("best_score"),
                          db.func.count(MockTest.id).label("tests_completed"))
        .join(MockTest, MockTest.user_id == User.id)
        .group_by(User.id)
        .order_by(db.desc("best_score"))
        .limit(50)
        .all()
    )
    return render_template("leaderboard.html", results=results)


# ------------------------------------------------------------------ profile
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user = current_user()
    if request.method == "POST":
        user.name = request.form.get("name", user.name)
        user.college = request.form.get("college", user.college)
        user.branch = request.form.get("branch", user.branch)
        user.year = request.form.get("year", user.year)
        user.skills = request.form.get("skills", user.skills)

        photo = request.files.get("profile_photo")
        if photo and photo.filename:
            filename = secure_filename(f"user_{user.id}_{photo.filename}")
            photo.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            user.profile_photo = filename

        resume = request.files.get("resume_file")
        if resume and resume.filename:
            filename = secure_filename(f"resume_{user.id}_{resume.filename}")
            resume.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            user.resume_file = filename

        db.session.commit()
        flash("Profile updated.", "success")
        return redirect(url_for("profile"))

    tests = MockTest.query.filter_by(user_id=user.id).order_by(MockTest.date.desc()).all()
    return render_template("profile.html", user=user, tests=tests)


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    from flask import send_from_directory
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/feedback", methods=["POST"])
@login_required
def feedback():
    message = request.form.get("message", "").strip()
    if message:
        db.session.add(Feedback(user_id=session["user_id"], message=message))
        db.session.commit()
        flash("Thank you for your feedback!", "success")
    return redirect(request.referrer or url_for("dashboard"))


# -------------------------------------------------------------------- admin
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email, is_admin=True).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            session["is_admin"] = True
            return redirect(url_for("admin_dashboard"))
        flash("Invalid admin credentials.", "danger")
    return render_template("admin/login.html")


@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    stats = {
        "users": User.query.count(),
        "questions": Question.query.count(),
        "coding_problems": CodingProblem.query.count(),
        "hr_questions": InterviewQuestion.query.count(),
        "mock_tests": MockTest.query.count(),
        "feedback": Feedback.query.count(),
    }
    return render_template("admin/dashboard.html", stats=stats)


@app.route("/admin/students")
@admin_required
def admin_students():
    students = User.query.filter_by(is_admin=False).all()
    return render_template("admin/students.html", students=students)


@app.route("/admin/students/delete/<int:user_id>")
@admin_required
def admin_delete_student(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("Student removed.", "info")
    return redirect(url_for("admin_students"))


@app.route("/admin/questions", methods=["GET", "POST"])
@admin_required
def admin_questions():
    if request.method == "POST":
        q = Question(
            section=request.form.get("section"),
            category=request.form.get("category"),
            question=request.form.get("question"),
            option1=request.form.get("option1"),
            option2=request.form.get("option2"),
            option3=request.form.get("option3"),
            option4=request.form.get("option4"),
            answer=request.form.get("answer"),
            difficulty=request.form.get("difficulty", "Easy"),
        )
        db.session.add(q)
        db.session.commit()
        flash("Question added.", "success")
        return redirect(url_for("admin_questions"))

    questions = Question.query.order_by(Question.id.desc()).all()
    return render_template("admin/questions.html", questions=questions)


@app.route("/admin/questions/delete/<int:qid>")
@admin_required
def admin_delete_question(qid):
    q = Question.query.get_or_404(qid)
    db.session.delete(q)
    db.session.commit()
    return redirect(url_for("admin_questions"))


@app.route("/admin/coding", methods=["GET", "POST"])
@admin_required
def admin_coding():
    if request.method == "POST":
        p = CodingProblem(
            title=request.form.get("title"),
            language=request.form.get("language"),
            difficulty=request.form.get("difficulty", "Easy"),
            description=request.form.get("description"),
            sample_input=request.form.get("sample_input"),
            sample_output=request.form.get("sample_output"),
            constraints=request.form.get("constraints"),
            hints=request.form.get("hints"),
            solution=request.form.get("solution"),
        )
        db.session.add(p)
        db.session.commit()
        flash("Coding problem added.", "success")
        return redirect(url_for("admin_coding"))

    problems = CodingProblem.query.order_by(CodingProblem.id.desc()).all()
    return render_template("admin/coding.html", problems=problems)


@app.route("/admin/coding/delete/<int:pid>")
@admin_required
def admin_delete_coding(pid):
    p = CodingProblem.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for("admin_coding"))


@app.route("/admin/hr-questions", methods=["GET", "POST"])
@admin_required
def admin_hr_questions():
    if request.method == "POST":
        q = InterviewQuestion(
            category=request.form.get("category"),
            question=request.form.get("question"),
            model_answer=request.form.get("model_answer"),
            tips=request.form.get("tips"),
            common_mistakes=request.form.get("common_mistakes"),
        )
        db.session.add(q)
        db.session.commit()
        flash("HR question added.", "success")
        return redirect(url_for("admin_hr_questions"))

    questions = InterviewQuestion.query.order_by(InterviewQuestion.id.desc()).all()
    return render_template("admin/hr_questions.html", questions=questions)


@app.route("/admin/hr-questions/delete/<int:qid>")
@admin_required
def admin_delete_hr_question(qid):
    q = InterviewQuestion.query.get_or_404(qid)
    db.session.delete(q)
    db.session.commit()
    return redirect(url_for("admin_hr_questions"))


@app.route("/admin/reports")
@admin_required
def admin_reports():
    tests = MockTest.query.order_by(MockTest.date.desc()).limit(100).all()
    return render_template("admin/reports.html", tests=tests)


@app.route("/admin/feedback")
@admin_required
def admin_feedback():
    items = Feedback.query.order_by(Feedback.created_at.desc()).all()
    return render_template("admin/feedback.html", items=items)


# ---------------------------------------------------------------- errors --
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
