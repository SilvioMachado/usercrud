from typing import Optional
from flask_sqlalchemy import SQLAlchemy

db: Optional[SQLAlchemy] = None


def init_from_app(app):
    global db
    db = SQLAlchemy(app)
