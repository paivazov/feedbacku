from django.db.models import Model, ForeignKey, CASCADE, DateTimeField

from feedbacks.models import User
from organisations.models import Organisation


class UserLastFeedbackInfo(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    organisation = ForeignKey(Organisation, on_delete=CASCADE)
    last_feedback_written_at = DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"Additional info about {self.user.get_full_name()} last feedback"
        )
