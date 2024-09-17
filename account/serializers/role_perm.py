from account.models.role_perm import RolePerm
from rest_framework import serializers
from .role import RoleSerializer
from .perm import PermSerializer


class RolePermSerializer(serializers.ModelSerializer):
    role_data = RoleSerializer(
        read_only=True,
        many=True
    )
    perm_data = PermSerializer(
        read_only=True,
        many=True
    )

    class Meta:
        model = RolePerm
        fields = [
            "id",
            "role",
            "perm",
            "value",
            "role_data",
            "perm_data"
        ]
