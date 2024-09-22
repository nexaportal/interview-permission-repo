from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from account.models.role import Role
from account.models.role_perm import RolePerm
from account.models.perm import Perm
from account.serializers.role_perm import RolePermSerializer
from account.serializers.role import RoleSerializer



class RoleViewSet(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=["get", "patch"], url_path="permission")
    def permission(self, request, pk=None):
        role = self.get_object()

        if request.method == "GET":
            # Handle GET request: Return permission list
            permissions = RolePerm.objects.filter(role=role)
            serializer = RolePermSerializer(permissions, many=True)
            return Response(serializer.data)

        elif request.method == "PATCH":
            # Handle PATCH request: Update permissions
            data = request.data.get("permissions", [])
            
            for perm_data in data:
                try:
                    perm = Perm.objects.get(id=perm_data["perm_id"])
                    role_perm, _ = RolePerm.objects.get_or_create(role=role, perm=perm)
                    role_perm.value = perm_data["value"]
                    role_perm.save()
                except Perm.DoesNotExist:
                    continue

            return Response({"status": "permissions updated"}, status=status.HTTP_200_OK)