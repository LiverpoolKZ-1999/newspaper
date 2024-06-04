import mimetypes
import os
from io import BytesIO
from typing import Any

import requests
from django.core.files.base import File
from django.db import transaction
from django.shortcuts import get_object_or_404

from app.common.models import TemporaryFile
from config import settings


@transaction.atomic
def temporary_file_create(*, file: Any):
    """
    Method creates a temporary file in aws s3 bucket.
    """
    temporary_file = TemporaryFile()
    temporary_file.file = file
    temporary_file.full_clean()
    temporary_file.save()
    return temporary_file


def temporary_file_get_content_as_file(
    file_uuid, delete_temp_file=True, need_file_name=False
):
    """
    Method gets a temporary file and returns it as a File object.
    Also deletes file from temporary storage after return.
    """
    temporary_file = get_object_or_404(TemporaryFile, file_uuid=file_uuid)

    bytes_io = BytesIO()

    if settings.IS_LOCAL:
        with open(temporary_file.file.path, "rb") as f:
            content = f.read()
            bytes_io.write(content)
        extension = os.path.splitext(temporary_file.file.path)[1]
        file_name = temporary_file.filename
    else:
        link = temporary_file.file.url
        response = requests.get(link)
        content_type = response.headers["content-type"]
        extension = mimetypes.guess_extension(content_type)
        bytes_io.write(response.content)
        file_name = temporary_file.filename

    if delete_temp_file:
        temporary_file.delete()

    if need_file_name:
        return File(bytes_io), file_name

    # NOTE: mimetypes default mapping do not include .zip extension so this is temp solution for zip format files
    if not extension:
        extension = f".{file_name.split('.')[-1]}"

    return File(bytes_io), extension
