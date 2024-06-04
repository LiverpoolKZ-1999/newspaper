from django.db import models
from django.utils.translation import gettext_lazy as _

from app.common.models import Timestamped


class Tag(Timestamped):
    name = models.CharField(verbose_name="name", max_length=50)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return f"tag - {self.name}"
