from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from model_utils.models import TimeStampedModel

from account.models import User

from .lang import Language


class Category(TimeStampedModel):
    items: models.QuerySet[CategoryItem]

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return f"Category #{self.pk}"


class CategoryItem(TimeStampedModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_("category"), related_name="items")
    lang = models.ForeignKey(
        Language, on_delete=models.DO_NOTHING, verbose_name=_("language"), related_name="lang_category_items"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("author"), related_name="category_items")

    name = models.CharField(max_length=200, verbose_name=_("name"))

    class Meta:
        verbose_name = _("category item")
        verbose_name_plural = _("category items")

    def __str__(self):
        return self.name
