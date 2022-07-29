from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, ListSerializer

from organisations.models import Organisation, Invitation

User = get_user_model()


class OrganisationConfigSerializer(ModelSerializer):
    class Meta:
        model = Organisation
        fields = ("name",)


class OrganisationInvitingSerializer(ModelSerializer):
    def validate(self, data):
        data["organisation_id"] = self.context.get("organisation_id")
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
