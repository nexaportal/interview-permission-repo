from account.models.perm import Perm
from rest_framework import serializers


class PermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perm
        fields = [
            "id",
            "name",
            "lang",
            "perm_model",
            "action",
            "field"
        ]
