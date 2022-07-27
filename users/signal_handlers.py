from uuid import uuid1

from django.conf.global_settings import AUTH_USER_MODEL
from django.db.models.signals import post_save
from django.dispatch import receiver

from organisations.models import Organisation


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_organisation_if_superuser(**kwargs):
    user = kwargs['instance']
    created = kwargs["created"]
    if created and user.is_superuser:
        Organisation.objects.create(
            manager=user, name=f"organisation {uuid1()}"
        )
