import uuid
import datetime
from app import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.Text)
    date = db.Column(db.DateTime)
    uuid = db.Column(db.String(36), unique=True)

    def __init__(self, title, body, date):
        self.title = title
        self.body = body
        self.date = datetime.datetime.strptime(date, "%d.%m.%Y")
        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return f"Post('{self.title}', '{self.date}', '{self.uuid}')"

    def to_json(self):
        return {
                   "title": self.title,
                   "body": self.body,
                   "date": str(self.date),
                   "uuid": self.uuid,
        }
