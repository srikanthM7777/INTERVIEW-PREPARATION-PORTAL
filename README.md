# Interview Preparation Portal

A full-stack web app for practicing aptitude, coding, HR and technical
interview questions, with mock tests, a leaderboard, student profiles,
and an admin panel — built with **Flask + SQLite + Bootstrap 5**.

## Tech Stack

- **Backend:** Python, Flask, Flask-SQLAlchemy
- **Database:** SQLite (default, zero setup) — easy to switch to MySQL, see below
- **Frontend:** HTML5, CSS3, Bootstrap 5, vanilla JavaScript
- **Auth:** Session-based login with hashed passwords (Werkzeug)

## Features

- Student registration / login / logout / forgot & change password
- Dashboard with progress stats and recent scores
- Aptitude practice (Quantitative, Logical Reasoning, Verbal, Data Interpretation, General Aptitude)
- Coding practice (Python, Java, C, C++, JavaScript) with hints & solutions
- HR interview question bank with model answers, tips and common mistakes
- Technical interview MCQs (DBMS, OS, Networking, Python, Java, HTML, CSS, JS, SQL)
- Full mock test: 30 random questions, 30-minute countdown timer, auto-submit, instant scoring
- Leaderboard ranked by best mock test score
- Profile page with photo upload, resume upload, and skills
- Admin panel: manage students, add/delete questions, coding problems, HR questions, view reports & feedback

## Project Structure

```
interview_prep_portal/
├── app.py                # Flask app & all routes
├── models.py             # SQLAlchemy models
├── config.py             # App configuration (DB URI, secret key, uploads)
├── seed.py                # Creates tables & inserts sample data + admin/demo accounts
├── requirements.txt
├── database/              # SQLite database file lives here
├── static/
│   ├── css/style.css
│   └── js/script.js
├── templates/
│   ├── base.html, index.html, login.html, register.html, ...
│   └── admin/              # Admin panel templates
└── uploads/                # Profile photos & resumes uploaded by users
```

## Getting Started

1. **Install dependencies** (Python 3.9+ recommended):
   ```bash
   pip install -r requirements.txt
   ```

2. **Create and seed the database** (run once):
   ```bash
   python seed.py
   ```
   This creates `database/portal.db` and adds sample questions, coding
   problems, HR questions, and two accounts:

   | Role  | Email             | Password  |
   |-------|-------------------|-----------|
   | Admin | admin@portal.com  | admin123  |
   | Demo student | demo@portal.com | demo123 |

3. **Run the app:**
   ```bash
   python app.py
   ```
   Then open **http://127.0.0.1:5000** in your browser.

4. To reset all data at any point, just run `python seed.py` again
   (it drops and recreates all tables).

## Switching to MySQL

By default the app uses SQLite so it runs with no extra setup. To use
MySQL instead:

1. Install the MySQL driver: `pip install pymysql`
2. Create a database in MySQL, e.g. `CREATE DATABASE interview_portal;`
3. In `config.py`, comment out the SQLite line and uncomment the MySQL
   line, filling in your username/password:
   ```python
   SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:YOUR_PASSWORD@localhost/interview_portal"
   ```
4. Run `python seed.py` again to create tables in MySQL.

## Notes for Resume / Interview Discussion

- Passwords are hashed with Werkzeug's `generate_password_hash` — never stored in plain text.
- Authentication uses Flask sessions; `@login_required` and `@admin_required` decorators protect routes.
- The same `Question` model and `quiz.html` template power both the Aptitude and Technical sections (and the Mock Test, which randomly samples from both) — a good example of DRY design.
- File uploads (profile photo, resume) are handled with `secure_filename` to prevent path traversal.
- The admin panel demonstrates full CRUD: add and delete questions, coding problems, and HR questions, plus read-only views of students, reports, and feedback.

## Ideas to Extend Further (Optional / Advanced)

- Email verification & real password-reset emails (e.g. via Flask-Mail)
- AI-powered answer feedback for HR responses
- Resume analyzer
- Company-wise question sets (TCS, Infosys, Wipro, Accenture, etc.)
- Dark mode toggle
- Certificates generated (PDF) after completing mock tests
- Charts of performance over time (Chart.js) on the dashboard
