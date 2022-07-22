from enum import Enum, unique

from rest_framework.permissions import BasePermission


class IsSuperuser(BasePermission):
    """
    Allows access only to superusers.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


@unique
class InvitationStates(Enum):
    created = "c"
    used = "u"
