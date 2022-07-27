from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_200_OK

from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import (
    MyTokenObtainPairSerializer,
    RegisterSerializer,
    RegistrationViaInvitationLinkSerializer,
)
from organisations.models import Invitation
from organisations.utils import InvitationStates
from users.services import create_new_user

User = get_user_model()


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class RegistrationViaInvitationLinkView(APIView):
    def post(self, request, invitation_id):
        invitation = get_object_or_404(Invitation, pk=invitation_id)
        if invitation.state == InvitationStates.used.value:
            return Response(
                {"detail": "This invitation link has been expired"},
                HTTP_403_FORBIDDEN,
            )
        serializer = RegistrationViaInvitationLinkSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data.update({"email": invitation.email})
        user = create_new_user(data)
        invitation.organisation.employees.add(user)
        invitation.state = InvitationStates.used.value
        invitation.save()
        return Response({"detail": "Operation successful"}, status=HTTP_200_OK)
