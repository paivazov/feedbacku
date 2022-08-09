from rest_framework.permissions import BasePermission


class IsManagerOrRecipient(BasePermission):
    """
    Allows access only to manager or definite user
    (recipient of current feedback) of current organisation.
    """

    message = (
        "This action is allowed only to manager of this company "
        "or feedback recipient."
    )

    def has_object_permission(self, request, view, obj):
        return obj.organisation.manager == request.user or (
            request.user == obj.recipient
        )
