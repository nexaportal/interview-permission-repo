from django.db import models
from django.utils.translation import gettext_lazy as _


class Language(models.Model):
    name = models.CharField(_("name"), max_length=100)
    code = models.CharField(_("code"), max_length=2)

    class Meta:
        db_table = "language"
        verbose_name = _("post")
        verbose_name_plural = _("posts")

    def __str__(self):
        return self.name
