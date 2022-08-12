from datetime import datetime
from flask import current_app
from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy(current_app)


class User(db.model):
    id = db.column(db.Integer, primary_key=True)
    company_name = db.column(db.String(80), nullable=False)
    phone = db.column(db.String(15), nullable=False)
    created = db.column(db.Datetime, default=datetime.utcnow)
    declared_billing = db.column(db.Integer)


