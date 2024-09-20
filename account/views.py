from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.authtoken.models import Token
from .models import Role, RolePerm
from rest_framework import viewsets, status
from django.contrib.auth import get_user_model
from account.permissions import HasRolePermission 
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from .controllers import RolePermController, RoleController, PermController
from .serializers import (
    RegisterSerializer, LoginSerializer, RolePermSerializer, RolePermUpdateSerializer,
    PermUpdateSerializer, PermSerializer
)



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


class RolePermViewSet(viewsets.ModelViewSet):
    serializer_class = RolePermSerializer
    queryset = RolePermController.list_role_perms()
    permission_classes = [IsAdminUser, ]

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return RolePermUpdateSerializer
        return self.serializer_class

    def list(self, request):
        queryset = RolePermController.list_role_perms()
        serializer = RolePermSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        serializer = RolePermSerializer(data=data)
        if serializer.is_valid():
            role_perm = serializer.save()  # This will now use the controller methods
            return Response(RolePermSerializer(role_perm).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        role_perm = RolePermController.get_role_perm(pk)
        if role_perm:
            serializer = RolePermSerializer(role_perm)
            return Response(serializer.data)
        return Response({"error": "RolePerm not found"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        deleted = RolePermController.delete_role_perm(pk)
        if deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "RolePerm not found"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['get'], url_path='permission', url_name='permission-list')
    def list_permissions(self, request, pk=None):
        """
        GET: /api/v1/role/<pk>/permission/
        Lists all permissions for the role with the given `pk`.
        """
        role_perm = RolePermController.get_role_perm(pk)
        if not role_perm:
            return Response({"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)

        # role_perms = RolePermController.filter_role_perms(role=role)
        serializer = RolePermSerializer(role_perm)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], url_path='update-permission', url_name='permission-update')
    def update_permissions(self, request, pk=None):
        """
        PATCH: /api/v1/role/<pk>/permission/
        Updates permissions for the role with the given `pk`.
        """
        role_perm = RolePermController.get_role_perm(pk)
        if not role_perm:
            return Response({"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)

        perm = role_perm.perm
        data = request.data
        updated_perm = PermController.update_perm(perm.id, data)
        serializer = PermSerializer(updated_perm)
        return Response(serializer.data, status=status.HTTP_200_OK)
