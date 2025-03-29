from flask_mail import Mail, Message
from flask import current_app

mail = Mail()

def send_email(recipient, subject, body):
    """Send an email using Flask-Mail."""
    msg = Message(subject, sender="admin@homicare.com", recipients=[recipient])
    msg.body = body
    with current_app.app_context():
        mail.send(msg)
