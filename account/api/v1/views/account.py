from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView

from account.api.v1.serializers import (
    LoginSerializer,
    LogoutSerializer,
)


class LoginView(TokenObtainPairView):
    """
    Authenticates with email and password then returns jwt tokens
    """

    serializer_class = LoginSerializer


class LogoutView(GenericAPIView):
    """
    Logs out a refresh token if it belongs to user of request.
    """

    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user)

        return Response(data=_("You logged out successfully."), status=status.HTTP_204_NO_CONTENT)
