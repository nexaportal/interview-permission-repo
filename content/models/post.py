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
    user = models.ForeignKey("account.User", on_delete=models.CASCADE, verbose_name=_("user"))
    post = models.ForeignKey(
        "content.POST", on_delete=models.CASCADE, verbose_name=_("post"), related_name="post_items"
    )
    lang = models.ForeignKey(
        "content.Language", on_delete=models.DO_NOTHING, verbose_name=_("language"), related_name="lang_items"
    )
    title = models.CharField(max_length=200, verbose_name=_("title"))
    content = models.TextField(verbose_name=_("content"))
    author = models.ForeignKey(AbstractUser, on_delete=models.CASCADE, verbose_name=_("author"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")
        unique_together = ("post", "lang")

    def __str__(self):
        return self.title
