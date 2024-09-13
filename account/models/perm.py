from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType


class PermissionActionChoices(models.TextChoices):
    LIST = ("list", _("LIST"))
    RETRIEVE = ("retrieve", _("RETRIEVE"))
    CREATE = ("create", _("CREATE"))
    UPDATE = ("update", _("UPDATE"))
    DELETE = ("delete", _("DELETE"))


class Perm(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=150, unique=True)
    codename = models.CharField(_("codename"), max_length=100)

    perm_model = models.ForeignKey(ContentType, models.CASCADE, verbose_name=_("model"), related_name="perm_model")
    action = models.CharField(choices=PermissionActionChoices.choices, verbose_name=_("action"), max_length=100)
    field = models.CharField(_("field"), max_length=100, blank=True, null=True)

    class Meta:
        db_table = "perm"
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"
        ordering = ["name"]

    def __str__(self):
        return f'{self.perm_model} | {self.name} | {self.lang.code if self.lang else "*"}'
