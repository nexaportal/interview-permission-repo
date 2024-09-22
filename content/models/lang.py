from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from .post import PostItem
    from .category import CategoryItem


class Language(models.Model):
    name = models.CharField(_("name"), max_length=100)
    code = models.CharField(_("code"), max_length=2)

    lang_post_items: models.QuerySet[PostItem]
    lang_category_items: models.QuerySet[CategoryItem]

    class Meta:
        verbose_name = _("language")
        verbose_name_plural = _("languages")

    def __str__(self):
        return f"{self.name} ({self.code})"

    @classmethod
    def get_by_code(cls, code: str):
        return cls.objects.filter(code=code).first()
