from django.contrib.auth import get_user_model, authenticate
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_403_FORBIDDEN,
    HTTP_200_OK,
    HTTP_201_CREATED,
)

from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import (
    MyTokenObtainPairSerializer,
    RegisterSerializer,
    RegistrationViaInvitationLinkSerializer,
    LoginViaInvitationLinkSerializer,
)
from users.services import create_new_user, InviteLinkEndpointMixin

User = get_user_model()


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class RegistrationViaInviteLinkView(APIView, InviteLinkEndpointMixin):
    def post(self, request, invitation_id):
        invitation = self.get_invitation_and_check_if_valid(invitation_id)
        serializer = RegistrationViaInvitationLinkSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data.update({"email": invitation.email})
        user = create_new_user(**data)
        self.add_user_to_organisation(invitation, user)

        return Response(
            self.construct_response(
                user,
                user_id=user.id,
                first_name=user.first_name,
            ),
            status=HTTP_201_CREATED,
        )


class LoginViaInviteLink(APIView, InviteLinkEndpointMixin):
    def post(self, request, invitation_id):
        serializer = LoginViaInvitationLinkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.validated_data

        user = authenticate(
            email=user_data['email'], password=user_data['password']
        )

        if not user:
            return Response(
                {"detail": "User with this credentials hasn't been found"},
                status=HTTP_403_FORBIDDEN,
            )

        invitation = self.get_invitation_and_check_if_valid(invitation_id)
        self.add_user_to_organisation(invitation, user)

        return Response(
            self.construct_response(
                user,
                user_id=user.id,
                first_name=user.first_name,
            ),
            status=HTTP_200_OK,
        )
