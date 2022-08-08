from django.contrib.auth import get_user_model
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

User = get_user_model()


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
    organisation = ForeignKey(Organisation, on_delete=CASCADE)
    sender = ForeignKey(User, on_delete=CASCADE, related_name="sender")
    recipient = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name="recipient",
    )

    def __str__(self):
        return f"{self.stars_amount} stars to {self.recipient.first_name}"
