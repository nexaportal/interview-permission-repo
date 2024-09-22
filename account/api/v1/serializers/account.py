from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainSerializer

from account.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "mobile", "first_name", "last_name")


class LoginSerializer(TokenObtainSerializer):
    username_field = "mobile"

    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True)

    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({"user": UserSerializer(self.user, context=self.context).data})
        data.update(self.user.get_jwt_tokens())

        update_last_login(None, self.user)

        return data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)

    def save(self, **kwargs):
        try:
            refresh_token = RefreshToken(self.validated_data["refresh"])

            if refresh_token.payload.get("user_id") != kwargs["user"].id:
                raise serializers.ValidationError(_("This token does not belong to you."))

            refresh_token.blacklist()
        except TokenError:
            pass
