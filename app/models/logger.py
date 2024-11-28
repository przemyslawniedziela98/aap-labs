from datetime import datetime
from .. import db


class AppLog(db.Model):
    """
    Database model for application logs.
    Stores log entries including timestamp, event type, and details.
    """
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    event_type = db.Column(db.String(50), nullable=False) 
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<AppLog {self.event_type}: {self.message[:50]}>"
