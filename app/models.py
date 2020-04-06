import uuid
import datetime
from app import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.Text)
    date = db.Column(db.DateTime)
    uuid = db.Column(db.String(36), unique=True)

    @property
    def pub_date(self):
        return self.date.strftime("%d.%m.%Y")

    @pub_date.setter
    def pub_date(self, date):
        self.date = datetime.datetime.strptime(date, "%d.%m.%Y")

    def __init__(self, title, body, date):
        self.title = title
        self.body = body
        # self.date = datetime.datetime.strptime(date, "%d.%m.%Y")
        self.pub_date = date
        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return f"Post('{self.title}', '{self.pub_date}', '{self.uuid}')"

    def to_json(self):
        return {
                   "title": self.title,
                   "body": self.body,
                   # "date": self.date,
                   "date": self.pub_date,
                   "uuid": self.uuid,
        }
