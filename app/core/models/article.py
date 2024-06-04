from django.db import models
from django.utils.translation import gettext_lazy as _

from app.common.models import Timestamped


class Article(Timestamped):
    name = models.TextField(verbose_name=_("name"), max_length=200)
    view_count = models.PositiveIntegerField(verbose_name=_("view count"), default=0)
    short_description = models.TextField(verbose_name=_("short description"))
    author = models.ForeignKey(
        to="core.Author",
        on_delete=models.SET_NULL,
        related_name="articles",
        verbose_name="author",
        null=True,
    )
    topic = models.ForeignKey(
        to="core.Topic",
        on_delete=models.SET_NULL,
        related_name="articles",
        verbose_name="topic",
        null=True,
    )
    tags = models.ManyToManyField(
        verbose_name=_("tags"),
        to="core.Tag",
        related_name="articles",
    )

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")

    def __str__(self):
        return f"article - {self.name}"
