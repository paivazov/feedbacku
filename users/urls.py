from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from users.views import (
    MyObtainTokenPairView,
    RegisterView,
    RegistrationViaInvitationLinkView,
)

urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token-obtain-pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('register/', RegisterView.as_view(), name='auth-register'),
    path(
        'register/<uuid:invitation_id>/',
        RegistrationViaInvitationLinkView.as_view(),
        name="register-via-invite-link",
    ),
]
