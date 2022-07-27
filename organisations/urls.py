from django.urls import path

from organisations.views import (
    OrganisationConfigView,
    OrganisationInvitingView,
)

urlpatterns = (
    path("edit/", OrganisationConfigView.as_view(), name="edit-organisation"),
    path("invite/", OrganisationInvitingView.as_view(), name="invite-member"),
)
