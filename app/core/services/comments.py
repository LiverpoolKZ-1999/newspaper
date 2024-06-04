from app.core.models import Article, Comment


def create_comment(*, name: str, article: Article) -> Comment:
    return Comment.objects.create(name=name, article=article)
