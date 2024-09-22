from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from model_utils.models import TimeStampedModel

from account.models import User

from .lang import Language


class Post(TimeStampedModel):
    items: models.QuerySet[PostItem]

    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")

    def __str__(self):
        en_item = self.items.filter(lang__code="en").first()
        return en_item.title if en_item else ""


class PostItem(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=_("post"), related_name="items")
    lang = models.ForeignKey(
        Language, on_delete=models.DO_NOTHING, verbose_name=_("language"), related_name="lang_post_items"
    )
    title = models.CharField(max_length=200, verbose_name=_("title"))
    content = models.TextField(verbose_name=_("content"))
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("author"), related_name="post_items")

    class Meta:
        verbose_name = _("post item")
        verbose_name_plural = _("post items")
        unique_together = ("post", "lang")

    def __str__(self):
        return self.title
