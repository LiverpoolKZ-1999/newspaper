from django.db import models
from django.utils.translation import gettext_lazy as _


class Timestamped(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("created_at"),
        verbose_name=_("created_at"),
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        help_text=_("modified_at"),
        verbose_name=_("modified_at"),
    )

    class Meta:
        abstract = True
