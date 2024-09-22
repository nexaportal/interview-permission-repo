from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from account.managers import UserManager


class User(AbstractUser):
    """Model definition for User."""

    """
    @TODO you should save mobile number without first zero.
            for example: 9112223344 (10 numbers)
    @TODO you should add validation for mobile `validate_mobile_number`
    """
    username = None
    USERNAME_FIELD = "mobile"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = UserManager()

    mobile = models.CharField(
        _("mobile"),
        max_length=10,
        unique=True
    )
    roles = models.ManyToManyField(
        "account.Role",
        related_name="users",
        blank=True
    )

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.mobile
