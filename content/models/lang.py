from django.db import models
from django.utils.translation import gettext_lazy as _


"""
    Language Added as an entity in the project not just a codename
"""


class Language(models.Model):
    name = models.CharField(_("name"), max_length=100)
    code = models.CharField(_("code"), max_length=2)

    class Meta:
        verbose_name = _("language")
        verbose_name_plural = _("languages")

    def __str__(self):
        return self.name
