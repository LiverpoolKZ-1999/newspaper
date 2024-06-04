from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CoreConfig(AppConfig):
    name: str = "app.core"
    verbose_name: str = _("core")
