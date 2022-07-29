from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    """
    Allows access only to managers.
    """

    def has_permission(self, request, view):
        if bool(request.user and request.user.is_superuser):
            return bool(
                request.user.organisation.id == view.kwargs.get("pk", None)
            )
        return False


class IsOrganisationMember(BasePermission):
    """
    Allows access only to members of current organisation.
    """

    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            pk = view.kwargs.get("pk", None)
            current_organisation = view.queryset.get(pk=pk)
            is_manager = bool(request.user == current_organisation.manager)
            is_member = bool(
                request.user in current_organisation.employees.all()
            )
            return bool(is_member or is_manager)
        return False


class ActionBasedPermission(BasePermission):
    """
    Grant or deny access to a view, based on a mapping in
    view.action_permissions
    """

    def has_permission(self, request, view):
        for klass, actions in getattr(view, 'action_permissions', {}).items():
            if view.action in actions:
                return klass().has_permission(request, view)
        return False
