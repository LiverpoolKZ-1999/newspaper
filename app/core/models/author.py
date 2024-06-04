from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from app.common.models import Timestamped


class Author(Timestamped):
    first_name = models.CharField(verbose_name=_("first name"), max_length=40)
    last_name = models.CharField(verbose_name=_("first name"), max_length=40)
    bio = models.TextField(verbose_name=_("bio"), null=True, blank=True)
    avatar = models.FileField(
        verbose_name=_("avatar"),
        upload_to="avatars/%Y/%m/%d/",
        blank=True,
        help_text=_("avatar"),
        validators=[FileExtensionValidator(allowed_extensions=["png", "jpeg", "jpg"])],
    )

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")

    def __str__(self):
        return f"{self.first_name} - {self.last_name}"
