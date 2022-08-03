from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from organisations.models import Organisation
from organisations.serializers import (
    OrganisationConfigSerializer,
    OrganisationInvitingSerializer,
    OrganisationMembersSerializer,
    OrganisationSerializer,
)
from organisations.permissions import IsManager, IsManagerOrOrganisationMember

User = get_user_model()


class OrganisationInvitingView(CreateAPIView):
    """Creates invitation."""

    serializer_class = OrganisationInvitingSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        context = super(
            OrganisationInvitingView, self
        ).get_serializer_context()
        context.update(
            {"organisation_id": self.kwargs.get("pk"), "request": self.request}
        )
        return context


class OrganisationConfigView(UpdateAPIView):
    """Provides editing organisation name.
    Contact phone, email of company can be implemented later"""

    permission_classes = (IsAuthenticated, IsManager)
    serializer_class = OrganisationConfigSerializer


class OrganisationMemberDeleteView(APIView):
    permission_classes = (IsAuthenticated, IsManager)

    def delete(self, request, organisation_id, user_id):
        organisation = Organisation.objects.prefetch_related("employees").get(
            pk=organisation_id
        )
        self.check_object_permissions(request, organisation)
        member = get_object_or_404(User, pk=user_id)
        organisation.employees.remove(member)

        return Response(
            {"detail": f"User {member.email} has been deleted successfully."},
            status=HTTP_204_NO_CONTENT,
        )


class OrganisationRetrieveListViewSet(ReadOnlyModelViewSet):
    """Provides next operations:
     - Lists all organisations.
     Allowed to any authenticated user.

     - Retrieves definite organisation and list of members of it.
    Allowed only to organisation members.
    """

    queryset = Organisation.objects.all()

    # .check_object_permissions() is not being checked automatically in list
    # views (has_object_permission() method in IsManager class). See:
    # https://www.django-rest-framework.org/api-guide/permissions/#limitations-of-object-level-permissions
    permission_classes = (IsAuthenticated, IsManagerOrOrganisationMember)

    def get_serializer_class(self):
        if self.action == "list":
            return OrganisationSerializer
        if self.action == "retrieve":
            return OrganisationMembersSerializer
