from django.db import models
from django.utils.translation import gettext_lazy as _

from app.common.models import Timestamped


class Comment(Timestamped):
    article = models.ForeignKey(
        to="core.Article",
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="article",
    )
    text = models.TextField(
        verbose_name=_("text"),
    )

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return f"comment - {self.created_at}"
