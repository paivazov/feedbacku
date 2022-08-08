from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.fields import Field, HiddenField
from rest_framework.serializers import ModelSerializer, CurrentUserDefault

from feedbacks.models import Feedback
from organisations.models import Organisation
from users.models import UserInfo

User = get_user_model()


class UserField(Field):
    default_error_messages = {
        "detail": "User with this email hasn't been found."
    }

    def to_representation(self, value):
        return {
            "id": value.id,
            "first_name": value.first_name,
            "last_name": value.last_name,
            "email": value.email,
        }

    def to_internal_value(self, email):
        validate_email(email)
        try:
            return User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise ValidationError(self.error_messages['detail'])


class FeedbackCreatingSerializer(ModelSerializer):
    recipient = UserField()
    sender = HiddenField(default=CurrentUserDefault())

    def validate(self, data):
        # refactor this.
        # The same on organisations.serializers.OrganisationInvitingSerializer
        organisation = get_object_or_404(
            Organisation, pk=self.context.get("organisation_id")
        )
        request = self.context.get("request")
        if organisation.manager != request.user and request.user not in (
            organisation.employees.all()
        ):
            raise PermissionDenied(
                "This action is allowed only to members of this company."
            )
        if data["recipient"] not in organisation.employees.all():
            raise ValidationError(
                {
                    "recipient": "This user isn't a member "
                    "of current organisation."
                },
            )
        data.update(
            {
                "organisation": organisation,
            }
        )
        return data

    class Meta:
        model = Feedback
        fields = (
            "is_anonymous",
            "stars_amount",
            "message",
            "recipient",
            "sender",
        )


class UserFeedbackSerializer(ModelSerializer):
    sender = UserField()

    class Meta:
        model = Feedback
        exclude = ("organisation", "recipient")


class UserInfoFeedbackSerializer(ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ("last_feedback_written_at",)
