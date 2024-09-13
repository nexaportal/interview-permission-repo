from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return f"Category #{self.id}"


class CategoryItem(models.Model):
    category = models.ForeignKey("content.POST", on_delete=models.CASCADE, verbose_name=_("post"))
    lang = models.ForeignKey(
        "content.Language",
        on_delete=models.DO_NOTHING,
        verbose_name=_("language"),
        related_name="category_lang_items",  # former related_name="lang_items"
    )
    author = models.ForeignKey("account.User", on_delete=models.CASCADE, verbose_name=_("author"))

    name = models.CharField(max_length=200, verbose_name=_("name"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        verbose_name = _("category item")
        verbose_name_plural = _("category items")

    def __str__(self):
        return self.name
