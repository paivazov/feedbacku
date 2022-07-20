from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from rest_framework.fields import EmailField, CharField
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Used for serializing user login data"""

    username_field = User.EMAIL_FIELD

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        token['username'] = user.username
        return token


class RegisterSerializer(ModelSerializer):
    email = EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    password = CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'email',
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
        if attrs['password'] != attrs['password2']:
            raise ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
