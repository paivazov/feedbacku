from uuid import uuid1

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from feedbacks.models import Feedback, UserLastFeedbackInfo
from organisations.models import Organisation


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_organisation_if_organisation_lead(**kwargs):
    """Handler that creates new organisation if newly created User
    is organisation lead"""
    user = kwargs['instance']
    created = kwargs["created"]
    if created and user.is_organisation_lead:
        Organisation.objects.create(
            manager=user, name=f"organisation {uuid1()}"
        )


@receiver(post_save, sender=Feedback)
def update_last_written_feedback_date(**kwargs):
    """Handler that updates info about User
    (when user last time wrote feedback)"""
    feedback = kwargs['instance']
    if kwargs["created"]:
        UserLastFeedbackInfo.objects.update_or_create(
            user=feedback.sender, organisation=feedback.organisation
        )
