from rest_framework.generics import UpdateAPIView, CreateAPIView

from organisations.models import Organisation
from organisations.serializers import (
    OrganisationConfigSerializer,
    OrganisationInvitingSerializer,
)
from organisations.utils import IsSuperuser


class OrganisationConfigView(UpdateAPIView):
    serializer_class = OrganisationConfigSerializer
    permission_classes = (IsSuperuser,)

    def get_object(self):
        return Organisation.objects.get(manager=self.request.user)


class OrganisationInvitingView(CreateAPIView):
    serializer_class = OrganisationInvitingSerializer
    permission_classes = (IsSuperuser,)

    def get_serializer_context(self):
        context = super(
            OrganisationInvitingView, self
        ).get_serializer_context()
        context.update({"user": self.request.user})
        return context
