from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

User = get_user_model()


def check_password_match(attrs: dict) -> dict:
    """Checks if passwords are the same.
    Args:
        attrs: dictionary of Serializer's data that need to be validated.
    Returns:
        dictionary of Serializer's data.
    Raises:
        ValidationError
    """
    if attrs['password'] != attrs['password2']:
        raise ValidationError({"password": "Password fields didn't match."})

    return attrs


def create_new_user(data: dict) -> User:
    """Creates new user.
    Args:
        data: dictionary of Serialized data.
    Returns:
        Newly created User object.
    """
    user = User.objects.create(
        username=data.get("email"),
        email=data.get("email"),
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        is_superuser=data.get("is_superuser", False),
    )

    user.set_password(data.get("password"))
    user.save()
    return user
