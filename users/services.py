from typing import Union
from uuid import UUID

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from organisations.models import Invitation
from organisations.utils import InvitationStates

User = get_user_model()


def check_password_match(attrs: dict) -> dict:
    """Checks if passwords are the same.
    Args:
        attrs: dictionary of Serializer's data that need to be validated.
    Returns:
        dictionary of Serializer's data.
    Raises:
        ValidationError.
    """
    if attrs['password'] != attrs['password2']:
        raise ValidationError({"password": "Password fields didn't match."})

    return attrs


def create_new_user(**kwargs) -> User:  # type: ignore
    """Creates new user.
    Args:
        kwargs: Serialized data.
    Returns:
        Newly created User object.
    """
    user = User.objects.create(
        username=kwargs.get("email"),
        email=kwargs.get("email"),
        first_name=kwargs.get("first_name"),
        last_name=kwargs.get("last_name"),
        is_superuser=kwargs.get("is_superuser", False),
    )

    user.set_password(kwargs.get("password"))
    user.save()
    return user


class InviteLinkEndpointMixin:
    def _get_user_token(self, user):
        # weird but this is in official docs
        # https://django-rest-framework-simplejwt.readthedocs.io/en/latest/creating_tokens_manually.html
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token), str(refresh)

    def get_invitation_and_check_if_valid(
        self,
        invitation_id: UUID,
    ) -> Union[Invitation, Response]:
        """Searches invitation and returns it if it's not used.
        Args:
            invitation_id: id of invitation we want to find.
        Returns:
            Invitation object.
        Raises:
            PermissionDenied if invitation has been used.
        """
        invitation = get_object_or_404(Invitation, pk=invitation_id)
        if invitation.state == InvitationStates.used.value:
            raise PermissionDenied(
                {"detail": "This invitation link has been expired"}
            )
        return invitation

    def add_user_to_organisation(
        self, invitation: Invitation, user: User  # type: ignore
    ) -> None:
        """Adds user to organisation which was in invitation
        and marks invitation as 'used'."""
        invitation.organisation.employees.add(user)
        invitation.state = InvitationStates.used.value
        invitation.save()

    def construct_response(self, user, **kwargs):
        """Makes response for user with access and refresh tokens."""
        access, refresh = self._get_user_token(user)
        return {'access': access, 'refresh': refresh, 'user_data': {**kwargs}}
