from uuid import uuid4

from django.conf import settings
from django.db.models import (
    Model,
    EmailField,
    CASCADE,
    CharField,
    OneToOneField,
    ManyToManyField,
    ForeignKey,
    UUIDField,
    DateField,
    BooleanField,
)

from organisations.utils import InvitationStates


class Organisation(Model):
    # manager can add itself to employees. Must be fixed
    name = CharField(max_length=120)
    manager = OneToOneField(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    employees = ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="many_users", blank=True
    )

    def __str__(self):
        return f'"{self.name}" organisation which belongs to {self.manager}'


class Department(Model):
    name = CharField(max_length=120)
    administrators = ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="admins"
    )
    members = ManyToManyField(settings.AUTH_USER_MODEL, related_name="members")
    organisation = ForeignKey(Organisation, on_delete=CASCADE)

    def __str__(self):
        return f'{self.name} department of {self.organisation} organisation.'


class Invitation(Model):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    email = EmailField()
    is_user_email_exists = BooleanField(default=False)
    created_at = DateField(auto_now=True)
    state = CharField(max_length=15, default=InvitationStates.created.value)
    organisation = ForeignKey(Organisation, on_delete=CASCADE)

    department = ForeignKey(Department, blank=True, on_delete=CASCADE)

    def __str__(self):
        if self.state == InvitationStates.created.value:
            return f"Created invitation for email {self.email}"
        else:
            return f"Accepted invitation for email {self.email}"
