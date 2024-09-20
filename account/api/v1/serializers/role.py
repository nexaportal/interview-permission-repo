from django.db import transaction

from rest_framework import serializers

from drf_extra_fields.relations import PresentablePrimaryKeyRelatedField

from account.models import Role, Perm, RolePerm


class PermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perm
        fields = "__all__"


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class RolePermListSerializer(serializers.ListSerializer):
    def save(self, **kwargs):
        role: Role = self.context["role"]
        with transaction.atomic():
            role.role_permset.all().delete()
            RolePerm.objects.bulk_create([RolePerm(role=role, **role_perm) for role_perm in self.validated_data])


class RolePermSerializer(serializers.ModelSerializer):
    perm = PresentablePrimaryKeyRelatedField(
        queryset=Perm.objects.all(),
        presentation_serializer=PermSerializer,
    )

    class Meta:
        model = RolePerm
        exclude = ("role",)
        list_serializer_class = RolePermListSerializer
