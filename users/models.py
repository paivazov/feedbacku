from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import DateTimeField, CharField, EmailField, BooleanField
from django.utils import timezone


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_organisation_lead", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_organisation_lead", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_organisation_lead") is not True:
            raise ValueError("Superuser must have is_organisation_lead=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = CharField("first name", max_length=150, blank=True)
    last_name = CharField("last name", max_length=150, blank=True)
    email = EmailField(
        "email address",
        blank=False,
        unique=True,
        error_messages={
            "unique": "A user with that email already exists.",
        },
    )
    date_joined = DateTimeField("date joined", default=timezone.now)
    is_active = BooleanField(
        "active",
        default=True,
        help_text="Designates whether this user should be treated as active. "
        "Unselect this instead of deleting accounts.",
    )
    is_organisation_lead = BooleanField(
        "organisation lead status",
        default=False,
        help_text="Designates whether the user can own an organisation "
        "in that site.",
    )
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    objects = UserManager()

    @property
    def is_staff(self):
        return self.is_organisation_lead

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
