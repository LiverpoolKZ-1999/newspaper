import os
import uuid

from django.core.files.storage import default_storage
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from storages.backends.s3boto3 import S3Boto3Storage

from config import settings

temporary_file_storage = (
    default_storage
    if settings.IS_LOCAL
    else S3Boto3Storage(bucket_name=settings.AWS_TEMP_STORAGE_BUCKET_NAME)
)


class TemporaryFile(models.Model):
    def temporary_file_upload_path(instance, filename):
        return f"temporary-files/{instance.file_uuid}/{filename}"

    file = models.FileField(
        upload_to=temporary_file_upload_path,
        verbose_name=_("temporary file"),
        storage=temporary_file_storage,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "png",
                    "jpeg",
                    "jpg",
                    "pdf",
                    "doc",
                    "docx",
                    "xls",
                    "xlsx",
                    "zip",
                    "csv",
                ]
            )
        ],
    )
    file_uuid = models.UUIDField(
        _("file uuid"), primary_key=True, default=uuid.uuid4, editable=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("created_at"),
        verbose_name=_("created_at"),
    )

    class Meta:
        verbose_name = _("temporary file")
        verbose_name_plural = _("temporary files")

    @property
    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return str(self.file_uuid)
