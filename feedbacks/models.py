from django.conf import settings
from django.db.models import (
    Model,
    PositiveSmallIntegerField,
    IntegerChoices,
    TextField,
    DateTimeField,
    ForeignKey,
    BooleanField,
    CASCADE,
)

from organisations.models import Organisation


class Feedback(Model):
    class StarsRange(IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    is_anonymous = BooleanField(default=False)
    stars_amount = PositiveSmallIntegerField(choices=StarsRange.choices)
    message = TextField(blank=True)
    created_at = DateTimeField(auto_now=True)
    sender = ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name="sender"
    )
    recipient = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name="recipient",
    )

    organisation = ForeignKey(Organisation, on_delete=CASCADE)

    def __str__(self):
        return f"{self.stars_amount} stars to {self.recipient.first_name}"


class UserLastFeedbackInfo(Model):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    organisation = ForeignKey(Organisation, on_delete=CASCADE)
    last_feedback_written_at = DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"Additional info about {self.user.get_full_name()} last feedback"
        )
