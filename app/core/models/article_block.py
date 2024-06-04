from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from app.common.models import Timestamped


class ArticleBlock(Timestamped):
    def image_upload_path(self, filename):
        return f"article/{self.article_id}/article-blocks/{self.order}/{filename}"

    article = models.ForeignKey(
        to="core.Article",
        on_delete=models.CASCADE,
        related_name="blocks",
        verbose_name="article",
    )
    order = models.PositiveIntegerField(verbose_name=_("order"))
    text = models.TextField(verbose_name=_("text"), null=True)
    background_text = models.CharField(
        verbose_name=_("background text"), max_length=100, null=True
    )
    video_url = models.TextField(verbose_name=_("video url"), null=True)
    image = models.FileField(
        verbose_name=_("avatar"),
        upload_to=image_upload_path,
        blank=True,
        null=True,
        help_text=_("avatar"),
        validators=[FileExtensionValidator(allowed_extensions=["png", "jpeg", "jpg"])],
    )
    text_tag = models.CharField(
        verbose_name=_("text position"), max_length=50, null=True
    )
    block_divider = models.BooleanField(
        verbose_name=_("block divider"),
        default=False,
    )

    class Meta:
        verbose_name = _("Article block")
        verbose_name_plural = _("Article blocks")

    def __str__(self):
        return f"blocks of article [{self.article.name}] - {self.order}"
