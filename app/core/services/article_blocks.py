from typing import Any, Dict, List, Optional

from django.db import transaction

from app.common.models import TemporaryFile
from app.common.services.temp_file_services import temporary_file_get_content_as_file
from app.core.models import Article, ArticleBlock


def create_article_block(
    *,
    article: Article,
    order: int,
    text: Optional[str] = None,
    background_text: Optional[str] = None,
    video_url: Optional[str] = None,
    image_url: Optional[TemporaryFile] = None,
    text_tag: Optional[str] = None,
    block_divider: Optional[str] = False,
):

    article_block = ArticleBlock(
        article=article,
        order=order,
        text=text,
        background_text=background_text,
        video_url=video_url,
        text_tag=text_tag,
        block_divider=block_divider,
    )
    file, file_name = temporary_file_get_content_as_file(
        image_url.file_uuid, need_file_name=True
    )
    article_block.image.save(file_name, file)
    article_block.refresh_from_db()
    return article_block


@transaction.atomic
def create_article_blocks(
    *,
    article: Article,
    blocks: List[Dict[str, Any]],
) -> List[ArticleBlock]:
    for block in blocks:
        article.refresh_from_db()
        create_article_block(**block)
    return article
