import smtplib
from email.message import EmailMessage
from celery import Celery

w = Celery("tasks")


@w.task
def send_emails(from_, emails, subj, post):
    s = smtplib.SMTP("localhost:8025")
    for email in emails:
        msg = EmailMessage()

        msg["From"] = from_
        msg["To"] = email
        msg["Subject"] = subj
        msg.set_content(post)

        s.send_message(msg)
    s.quit()
