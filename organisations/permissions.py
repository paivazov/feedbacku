from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    """
    Allows access only to managers of current organisation.
    """

    message = "This action is allowed only to managers of this company."

    def has_object_permission(self, request, view, obj):
        return obj.manager == request.user


class IsManagerOrOrganisationMember(BasePermission):
    """
    Allows access only to manager or members of current organisation.
    """

    message = "This action is allowed only to members of this company."

    def has_object_permission(self, request, view, obj):
        return obj.manager == request.user or request.user in obj.employees
