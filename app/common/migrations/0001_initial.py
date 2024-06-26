# Generated by Django 3.2.4 on 2024-06-04 11:54

import uuid

import django.core.validators
from django.db import migrations, models

import app.common.models.temp_files


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TemporaryFile",
            fields=[
                (
                    "file",
                    models.FileField(
                        upload_to=app.common.models.temp_files.TemporaryFile.temporary_file_upload_path,
                        validators=[
                            django.core.validators.FileExtensionValidator(
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
                        verbose_name="temporary file",
                    ),
                ),
                (
                    "file_uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="file uuid",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="created_at",
                        verbose_name="created_at",
                    ),
                ),
            ],
            options={
                "verbose_name": "temporary file",
                "verbose_name_plural": "temporary files",
            },
        ),
    ]
