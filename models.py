from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    college = db.Column(db.String(150))
    branch = db.Column(db.String(100))
    year = db.Column(db.String(20))
    profile_photo = db.Column(db.String(255), default="default.png")
    skills = db.Column(db.String(255))
    resume_file = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    mock_tests = db.relationship("MockTest", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Question(db.Model):
    """Generic MCQ question used for Aptitude and Technical sections."""
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(30), nullable=False)   # 'aptitude' or 'technical'
    category = db.Column(db.String(60), nullable=False)  # e.g. Quantitative, DBMS, Python
    question = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(255))
    option2 = db.Column(db.String(255))
    option3 = db.Column(db.String(255))
    option4 = db.Column(db.String(255))
    answer = db.Column(db.String(255))  # correct option text
    difficulty = db.Column(db.String(20), default="Easy")


class CodingProblem(db.Model):
    __tablename__ = "coding_problems"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    language = db.Column(db.String(50), default="Any")
    difficulty = db.Column(db.String(20), default="Easy")
    description = db.Column(db.Text)
    sample_input = db.Column(db.Text)
    sample_output = db.Column(db.Text)
    constraints = db.Column(db.Text)
    hints = db.Column(db.Text)
    solution = db.Column(db.Text)


class InterviewQuestion(db.Model):
    """HR interview questions."""
    __tablename__ = "interview_questions"
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100))
    question = db.Column(db.Text, nullable=False)
    model_answer = db.Column(db.Text)
    tips = db.Column(db.Text)
    common_mistakes = db.Column(db.Text)


class MockTest(db.Model):
    __tablename__ = "mock_tests"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    score = db.Column(db.Integer, default=0)
    total = db.Column(db.Integer, default=30)
    time_taken = db.Column(db.Integer)  # seconds
    date = db.Column(db.DateTime, default=datetime.utcnow)


class Feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User")
