import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = "change-this-secret-key-in-production"

    # ---- Default: SQLite (zero setup, works immediately) ----
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "database", "portal.db")

    # ---- To use MySQL instead, comment the line above and uncomment below ----
    # Requires: pip install pymysql
    # SQLALCHEMY_DATABASE_URI = (
    #     "mysql+pymysql://root:YOUR_PASSWORD@localhost/interview_portal"
    # )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB uploads
