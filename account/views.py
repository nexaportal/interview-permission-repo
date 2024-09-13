from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "user": {
                "mobile": user.mobile,
                "first_name": user.first_name,
                "last_name": user.last_name
            },
            "token": token.key
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        login(request, user)

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "user": {
                "mobile": user.mobile,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        }, status=status.HTTP_200_OK)
