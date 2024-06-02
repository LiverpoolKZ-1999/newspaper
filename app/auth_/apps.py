from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuthConfig(AppConfig):
    name: str = "app.auth_"
    verbose_name: str = _("auth_")
