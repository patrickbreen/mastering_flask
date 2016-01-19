import smtplib
from email.mime.text import MIMEText
from flask import render_template

from webapp.extensions import celery
from webapp.models import Reminder

from mail import email_addr, password

def email(email, password, subject, text,
        to, server_addr='smtp.gmail.com:587'):

    MIMEText(text)
    msg['Subject'] = subject
    msg['From'] = email

    smtp_server = smtplib.SMTP(server_addr)
    smtp_server.starttls()
    smtp_server.login(email, password)
    smtp_server.sendmail(
            email,
            to,
            msg.as_string()
            )
    smtp.server.close()

@celery.task(
        bind=True,
        ignore_result=True,
        default_retry_delay=3000,
        max_retries=5)
def remind(self, pk):
    reminder = Reminder.query.get(pk)
    email(email=email_addr,
            password=password,
            subject = "your reminder",
            text=reminder.text,
            to=reminder.email)

    return


