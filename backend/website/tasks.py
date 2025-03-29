from datetime import datetime, timedelta, timezone
from website import create_app, db
from .models import Service_Requests, Service_Professionals
from .email_utils import send_email
from .celery_config import make_celery

app = create_app()
celery = make_celery(app)

@celery.task
def send_reminder_emails():
    """Send reminder emails to service professionals with pending requests."""
    with app.app_context():
        now_utc = datetime.now(timezone.utc)  # ✅ Timezone-aware datetime
        time_threshold = now_utc - timedelta(days=1)

        # Get service requests that are still pending for more than 24 hours
        pending_requests = Service_Requests.query.filter(
            Service_Requests.Status == "pending",
            Service_Requests.Start_date < time_threshold  # Using Start_date
        ).all()
        # Find professionals with pending requests
        professionals = {req.Professional_id for req in pending_requests}

        for prof_id in professionals:
            professional = Service_Professionals.query.filter_by(Professional_id=prof_id).first()
            if professional:
                send_email(
                    recipient=professional.Email,
                    subject="Reminder: Pending Service Requests",
                    body=f"Dear {professional.Name},\n\n"
                         "You have pending service requests that require your attention. "
                         "Please log in to your dashboard and respond to them.\n\n"
                         "Best regards,\nHomiCare Team"
                )

    return f"Sent {len(professionals)} reminder emails."
