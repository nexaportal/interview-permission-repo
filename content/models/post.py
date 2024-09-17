from django.db import models
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")

    def __str__(self):
        post_items = self.post_items.filter(lang__code="en")
        return ",".join(item.title for item in post_items)


class PostItem(models.Model):
    post = models.ForeignKey(
        "content.POST", on_delete=models.CASCADE, verbose_name=_("post"), related_name="post_items"
    )
    lang = models.ForeignKey(
        "content.Language", on_delete=models.DO_NOTHING, verbose_name=_("language"), related_name="lang_post_items"
    )
    title = models.CharField(max_length=200, verbose_name=_("title"))
    content = models.TextField(verbose_name=_("content"))
    author = models.ForeignKey("account.User", on_delete=models.CASCADE, verbose_name=_("author"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        verbose_name = _("postitem")
        verbose_name_plural = _("postitems")
        unique_together = ("post", "lang")

    def __str__(self):
        return self.title
