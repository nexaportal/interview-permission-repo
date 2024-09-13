from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")

    def __str__(self):
        return self.items.filter(lang="en")


class PostItem(models.Model):
    user = models.ForeignKey(
        "account.User",
        on_delete=models.CASCADE,
        verbose_name=_("user"),
        related_name="user_post_items",  # Add related_name to avoid clash
    )
    post = models.ForeignKey(
        "content.POST", on_delete=models.CASCADE, verbose_name=_("post"), related_name="post_items"
    )
    lang = models.ForeignKey(
        "content.Language", on_delete=models.DO_NOTHING, verbose_name=_("language"), related_name="post_items"
    )
    title = models.CharField(max_length=200, verbose_name=_("title"))
    content = models.TextField(verbose_name=_("content"))
    author = models.ForeignKey(
        "account.User",
        on_delete=models.CASCADE,
        verbose_name=_("author"),
        related_name="author_post_items",  # Add related_name to avoid clash
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        verbose_name = _("post item")
        verbose_name_plural = _("post items")
        unique_together = ("post", "lang")

    def __str__(self):
        return self.title
