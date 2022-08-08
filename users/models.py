from django.contrib.auth import get_user_model
from django.db.models import Model, CASCADE, OneToOneField, DateTimeField

User = get_user_model()


class UserInfo(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    last_feedback_written_at = DateTimeField(auto_now=True)

    def __str__(self):
        return f"Additional info about {self.user.get_full_name()}"
