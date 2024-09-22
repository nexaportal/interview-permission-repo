from account.models.role_perm import RolePerm
from rest_framework import serializers
from .role import RoleSerializer
from .perm import PermSerializer
from account.models.role import Role
from account.models.perm import Perm


class RolePermSerializer(serializers.ModelSerializer):
    role_data = serializers.SerializerMethodField()
    perm_data = serializers.SerializerMethodField()

    def get_role_data(self, obj):
        role_data = Role.objects.filter(id=obj.role.id)
        return RoleSerializer(role_data, many=True).data

    def get_perm_data(self, obj):
        perm_data = Perm.objects.filter(id=obj.perm.id)
        return PermSerializer(perm_data, many=True).data
        
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
