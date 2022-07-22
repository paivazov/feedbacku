from django.urls import path

from organisations.views import (
    OrganisationConfigView,
    OrganisationInvitingView,
)

urlpatterns = (
    path("edit/", OrganisationConfigView.as_view()),
    path("invite/", OrganisationInvitingView.as_view()),
)
