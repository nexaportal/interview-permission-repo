from account.serializers.user import MyTokenObtainPairSerializer,\
    RegisterSerializer
from account.models.user import User
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import generics, status

"""
    This View Will Generate Bearer Token For User
    Based on their credentials with expiration for the token
    request data:
        - mobile
        - password
"""


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        request.data["mobile"] = request.data["mobile"].lower()
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            print(e)
            return Response(
                {
                    "detail": "User Credential is not valid",
                    "status": 401
                },
                    status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

"""
    View To Register User 
    request data:
        - mobile
        - first_name
        - last_name
        - password
        - email
"""
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_data = RegisterSerializer(user).data

        return Response(
            {
                "status": "success",
                "message": "User registered successfully.",
                "data": user_data
            },
            status=status.HTTP_201_CREATED,
        )
