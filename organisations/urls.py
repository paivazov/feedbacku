from django.urls import path, include
from rest_framework.routers import SimpleRouter

from organisations.views import (
    OrganisationRetrieveListViewSet,
    OrganisationConfigView,
    OrganisationMemberDeleteView,
    OrganisationInvitingView,
)

router = SimpleRouter(trailing_slash=False)
router.register('', OrganisationRetrieveListViewSet)

urlpatterns = (
    path("", include(router.urls)),
    path(
        "<int:pk>/",
        OrganisationConfigView.as_view(),
        name="config-organisation",
    ),
    path(
        "<int:pk>/users/invite/",
        OrganisationInvitingView.as_view(),
        name="invite-member",
    ),
    path(
        "<int:organisation_id>/users/<int:user_id>/",
        OrganisationMemberDeleteView.as_view(),
        name="delete-member",
    ),
)
