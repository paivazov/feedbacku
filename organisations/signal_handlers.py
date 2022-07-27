from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from organisations.models import Invitation
from organisations.tasks import send_email
from organisations.services import get_url_path


@receiver(post_save, sender=Invitation)
def send_invitation_mail(**kwargs):
    """Handler that sends email after creating invitation"""
    invitation = kwargs['instance']
    created = kwargs["created"]

    subject = "FeedbackU invitation"
    message = (
        f"Hello! You have been invited to {invitation.organisation.name}! \n"
        "To accept invitation, please follow this link: "
        f"{get_url_path('register-via-invite-link', (invitation.id,))}"
    )
    if created:
        send_email.delay(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            (invitation.email,),
        )
