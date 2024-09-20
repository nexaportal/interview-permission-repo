from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from .role_perm import RolePerm


class Role(models.Model):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=150,
        unique=True,
    )

    role_permset: models.QuerySet[RolePerm]

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        ordering = ["name"]

    def __str__(self):
        return self.name
