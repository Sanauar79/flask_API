from flask_mail import Message
from app.extensions import mail

def send_email_to_user(name, email):
    subject = "Thanks for contacting us"
    body = f"Hi {name}, we've received your message!"
    send_email(email, subject, body)

def send_email_to_admin(name, email, phone, message):
    subject = "New Contact Form Submission"
    body = f"{name} ({email}, {phone}) says:\n{message}"
    send_email("sanauarh@gmail.com", subject, body)

def send_email(to, subject, body):
    msg = Message(subject=subject, recipients=[to], body=body)
    mail.send(msg)
