from typing import Union

from django.db.models import QuerySet
from rest_framework.response import Response

from feedbacks.models import Feedback


def get_filtered_feedbacks(
    organisation_id: int, recipient_id: int
) -> Union[QuerySet, Response]:
    """Filters feedbacks and sorts in descending of creation"""
    queryset = Feedback.objects.filter(
        organisation_id=organisation_id,
        recipient_id=recipient_id,
    )
    return queryset.order_by("-created_at")


def get_object_or_none(model, **kwargs) -> Union[QuerySet, None]:
    """
    Args:
        model: Model instance
        kwargs: The lookup parameters
    Returns:
        Object or None if it hasn't been found"""
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None


def make_senders_anonymous(queryset) -> None:
    """Checks if sender wants to be anon in each object in queryset
    (without saving it in a database) and switches sender to None in needed"""
    for obj in queryset:
        if obj.is_anonymous:
            obj.sender = None
