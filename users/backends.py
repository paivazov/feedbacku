from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

User = get_user_model()


class AuthenticationBackend(BaseBackend):
    """
    Authentication Backend
    :To manage the authentication process of user using email
    instead of username
    """

    @staticmethod
    def _can_authenticate(user):
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        return user if self._can_authenticate(user) else None

    def authenticate(self, request, email=None, password=None):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        if user.check_password(password) and self._can_authenticate(user):
            return user
        return None
