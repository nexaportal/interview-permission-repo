from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    mobile = models.CharField(
        _("mobile"),
        max_length=10,
        unique=True,
    )
    role_perms = models.ManyToManyField(
        "account.RolePerm", verbose_name=_("roleperms"), related_name="users_roleperms"
    )

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username
