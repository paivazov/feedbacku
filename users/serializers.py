from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.fields import EmailField, CharField, HiddenField
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.validators import UniqueValidator

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.services import check_password_match, create_new_user

User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Used for serializing user login data"""

    username_field = User.EMAIL_FIELD

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        token['email'] = user.email
        return token


class RegisterSerializer(Serializer):
    email = EmailField(
        required=True,
        validators=(UniqueValidator(queryset=User.objects.all()),),
    )
    first_name = CharField(max_length=120, write_only=True, required=True)
    last_name = CharField(max_length=120, write_only=True, required=True)
    password = CharField(
        write_only=True, required=True, validators=(validate_password,)
    )
    password2 = CharField(write_only=True, required=True)
    is_organisation_lead = HiddenField(default=True)

    def validate(self, attrs):
        return check_password_match(attrs)

    def create(self, validated_data):
        return create_new_user(**validated_data)


class RegistrationViaInvitationLinkSerializer(ModelSerializer):
    password = CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'password',
            'password2',
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        return check_password_match(attrs)


class LoginViaInvitationLinkSerializer(Serializer):
    email = EmailField(
        required=True,
        write_only=True,
    )
    password = CharField(
        required=True, write_only=True, validators=(validate_password,)
    )
