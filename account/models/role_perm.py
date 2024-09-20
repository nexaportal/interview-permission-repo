from django.db import models
from django.utils.translation import gettext_lazy as _


class RolePerm(models.Model):
    role = models.ForeignKey(
        "account.Role", on_delete=models.CASCADE, verbose_name=_("role"), related_name="role_permset"
    )
    perm = models.ForeignKey(
        "account.Perm", on_delete=models.CASCADE, verbose_name=_("perm"), related_name="perm_permset"
    )
    value = models.BooleanField(default=True, verbose_name=_("has perm"))

    class Meta:
        verbose_name = _("role_perm")
        verbose_name_plural = _("role_perms")
        unique_together = ("role", "perm")
        ordering = ["role", "perm"]

    def __str__(self):
        return f"{self.role} | {self.perm} | {str(self.value)}"
