from uuid import uuid1

from django.conf.global_settings import AUTH_USER_MODEL
from django.db.models.signals import post_save
from django.dispatch import receiver

from feedbacks.models import Feedback
from organisations.models import Organisation
from users.models import UserLastFeedbackInfo


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_organisation_if_superuser(**kwargs):
    """Handler that creates new organisation if newly created User
    is manager"""
    user = kwargs['instance']
    created = kwargs["created"]
    if created and user.is_superuser:
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
