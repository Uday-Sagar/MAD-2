from celery.schedules import crontab
from celery import Celery
from flask import Flask
import os

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6340/0"),
        backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6340/0"),
        include=["website.tasks"]
    )
    celery.conf.update(app.config)

    celery.conf.beat_schedule = {
        "send-daily-reminders": {
            "task": "website.tasks.send_reminder_emails",
            "schedule": crontab(hour=20, minute=0),  # Runs every day at 9 AM
        }
    }
    return celery