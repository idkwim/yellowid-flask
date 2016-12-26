from app import db
from datetime import datetime, timedelta


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_key = db.Column(db.String(32), index=True, unique=True)
    join_date = db.Column(db.String())
    last_active_date = db.Column(db.String())

    def __init__(self, user_key):
        self.user_key = user_key
        self.join_date = datetime.strftime(
            datetime.utcnow() + timedelta(hours=9),
            "%Y.%m.%d %H:%M:%S")
        self.last_active_date = self.join_date

    def __repr__(self):
        return "<User %r>" % (self.user_key)
