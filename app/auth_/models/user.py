import logging
import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _

from app.common.models import Timestamped

logger = logging.getLogger(__name__)


class CustomUserManager(BaseUserManager):
    def get_by_natural_key(self, email):
        return self.get(email=email)


class User(Timestamped, PermissionsMixin, AbstractBaseUser):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    email = models.EmailField(_("email"), unique=True)
    is_active = models.BooleanField(_("is_active"), default=True)
    is_staff = models.BooleanField(_("is_staff"), default=False)

    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email
