from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from .role import Role


class User(AbstractUser):
    """Model definition for User."""

    mobile = PhoneNumberField(unique=True)
    roles = models.ManyToManyField(Role, blank=True)

    def __str__(self):
        return str(self.mobile)

    def get_jwt_tokens(self):
        token = (
            OutstandingToken.objects.filter(user=self, expires_at__gt=timezone.now(), blacklistedtoken__isnull=True)
            .order_by("-created_at")
            .first()
        )

        refresh = RefreshToken.for_user(self) if not token else RefreshToken(token.token)

        return {"refresh": str(refresh), "access": str(refresh.access_token)}
