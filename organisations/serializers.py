from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from feedbacks.services import get_object_or_none
from organisations.models import Organisation, Invitation

User = get_user_model()


class OrganisationConfigSerializer(ModelSerializer):
    class Meta:
        model = Organisation
        fields = ("name",)


class OrganisationInvitingSerializer(ModelSerializer):
    def validate(self, data):
        # refactor this.
        # The same on feedbacks.serializers.FeedbackCreatingSerializer
        organisation = get_object_or_404(
            Organisation, pk=self.context.get("organisation_id")
        )

        # Permission check has been moved to serializer in order to
        # Generic create views supports object-level restrictions only in
        # serializers. See:
        # https://www.django-rest-framework.org/api-guide/permissions/#overview-of-access-restriction-methods
        if self.context.get("request").user != organisation.manager:
            raise PermissionDenied(
                "This action is allowed only to managers of this company."
            )

        # checks if user with this email has been registered earlier
        user = get_object_or_none(User, email=data.get("email"))
        if user:
            data["is_user_email_exists"] = True
        else:
            data["is_user_email_exists"] = False

        data["organisation"] = organisation
        return data

    class Meta:
        model = Invitation
        fields = ("email",)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email")


class OrganisationMembersSerializer(ModelSerializer):
    employees = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Organisation
        fields = ("id", "name", "employees")


class OrganisationSerializer(ModelSerializer):
    quantity_of_employees = SerializerMethodField()
    manager = UserSerializer(read_only=True)

    @staticmethod
    def get_quantity_of_employees(org):
        return org.employees.all().count()

    class Meta:
        model = Organisation
        fields = ("id", "name", "manager", "quantity_of_employees")
