from django.db import models
from django.utils.translation import gettext_lazy as _


class Role(models.Model):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=150,
        unique=True,
    )

    class Meta:
        db_table = "role"
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        ordering = ["name"]

    def __str__(self):
        return self.name
