from typing import Any, Dict, List, Optional

from django.db import transaction

from app.core.models import Article, Author, Tag, Topic
from app.core.services import create_article_blocks


@transaction.atomic
def article_create(
    *,
    name: str,
    short_description: str,
    author: Author,
    topic: Topic,
    blocks: List[Dict[str, Any]],
    tags: Optional[List[Tag]] = None,
) -> Article:
    article = Article.objects.create(
        name=name,
        short_description=short_description,
        author_id=author.id,
        topic_id=topic.id,
    )
    article.tags.set(tags)
    create_article_blocks(article=article, blocks=blocks)

    return article


@transaction.atomic
def article_update(
    *,
    article: Article,
    article_data: Optional[Dict[str, Any]] = None,
    article_blocks: Optional[List[Dict[str, Any]]] = None,
) -> Article:
    article.refresh_from_db()

    return article


def article_list():
    return Article.objects.select_related("topic", "author").prefetch_related("tags")


@transaction.atomic
def article_delete(
    *,
    article: Article,
) -> Article:
    article.delete()
