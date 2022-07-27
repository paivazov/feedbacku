import datetime
from typing import Union

from django.core.mail import send_mail
from django.utils import timezone

from FeedbackU.celery import app
from organisations.models import Invitation


@app.task
def send_email(
    subject: str,
    message: str,
    from_email: str,
    recipients: Union[list, tuple],
) -> None:
    """sends regular Django email using task queue"""
    print("hello")
    send_mail(
        subject,
        message,
        from_email,
        recipients,
    )


@app.task
def erase_old_invitations() -> None:
    """Deletes all invitations that are older than 30 days"""
    overdue_invitations = Invitation.objects.filter(
        created_at__lt=timezone.now() - datetime.timedelta(days=30)
    )
    overdue_invitations.delete()
