from django.db.models import Exists
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from organisations.models import Organisation, Invitation


class OrganisationConfigSerializer(ModelSerializer):
    class Meta:
        model = Organisation
        fields = ("name",)


class OrganisationInvitingSerializer(ModelSerializer):
    def validate(self, data):
        """
        Check that start is before finish.
        """
        organisation = Organisation.objects.get(manager=self.context['user'])
        if not organisation:
            raise ValidationError(
                "You don't have permission to invite employees "
                "in this organisation."
            )
        data["organisation"] = organisation
        return data

    class Meta:
        model = Invitation
        fields = ("email",)
