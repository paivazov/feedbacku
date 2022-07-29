from django.urls import path, include
from rest_framework.routers import SimpleRouter

from organisations.views import OrganisationInvitingView, OrganisationViewSet

router = SimpleRouter(trailing_slash=False)
router.register('', OrganisationViewSet)

urlpatterns = (
    path("", include(router.urls)),
    path(
        "<int:pk>/invite",
        OrganisationInvitingView.as_view(),
        name="invite-member",
    ),
)
