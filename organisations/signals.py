from django.conf.global_settings import AUTH_USER_MODEL
from django.core.mail import BadHeaderError, send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from rest_framework.response import Response

from organisations.models import Invitation

# WIP HERE!!!!
@receiver(pre_save, sender=AUTH_USER_MODEL)
def create_organisation_if_superuser(**kwargs):
    invitation = kwargs['instance']
    created = kwargs["created"]

    subject = f"Hello! You have been invited to organisation"

    if created:
        try:
            send_mail(subject, message, from_email, ['admin@example.com'])
        except BadHeaderError:
            return Response({"detail": 'Invalid header found.'})
