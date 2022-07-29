from rest_framework.generics import CreateAPIView
from rest_framework.mixins import (
    ListModelMixin,
    UpdateModelMixin,
    RetrieveModelMixin,
)
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from organisations.models import Organisation
from organisations.serializers import (
    OrganisationConfigSerializer,
    OrganisationInvitingSerializer,
    OrganisationMembersSerializer,
    OrganisationSerializer,
)
from organisations.permissions import (
    IsManager,
    ActionBasedPermission,
    IsOrganisationMember,
)


class OrganisationInvitingView(CreateAPIView):
    serializer_class = OrganisationInvitingSerializer
    permission_classes = (IsManager,)

    def get_serializer_context(self):
        context = super(
            OrganisationInvitingView, self
        ).get_serializer_context()
        context.update({"organisation_id": self.kwargs.get("pk")})
        return context


class OrganisationViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    queryset = Organisation.objects.all()

    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        IsAuthenticated: ("list",),
        IsOrganisationMember: ("retrieve",),
        IsManager: ("update",),
    }

    def get_serializer_class(self):
        if self.action == "list":
            return OrganisationSerializer
        if self.action == "retrieve":
            return OrganisationMembersSerializer
        if self.action == "update":
            return OrganisationConfigSerializer
