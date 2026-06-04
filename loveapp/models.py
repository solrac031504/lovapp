from datetime import datetime

from extensions import db
from flask_login import UserMixin

"""Represents """


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    login_count = db.Column(db.Integer, default=0, nullable=False)
    last_login_utc = db.Column(db.DateTime, nullable=True)
    send_email = db.Column(db.Boolean, default=True, nullable=False)
    send_message = db.Column(db.Boolean, default=True, nullable=False)


class CalendarEventType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(100))


class CalendarEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_type_id = db.Column(db.Integer, db.ForeignKey("calendar_event_type.id"))
    is_all_day = db.Column(db.Boolean)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.now())


class EmailNotification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    notif_type = db.Column(db.String(50))  # 'event', 'complaint', 'system'


class TextNotification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    notif_type = db.Column(db.String(50))  # 'event', 'complaint', 'system'


class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    submitter_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    mood = db.Column(db.String(50))  # 'frustrated', 'sad', 'upset'
    status = db.Column(db.String(50), default="open")  # open, acknowledged, resolved
    severity_level = db.Column(db.Integer)  # 1-10
    created_at = db.Column(db.DateTime, default=datetime.now())
