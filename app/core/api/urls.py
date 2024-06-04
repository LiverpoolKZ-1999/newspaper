from django.urls import path

from .views import (
    ArticleCreateApi,
    ArticleDeleteApi,
    ArticleListApi,
    ArticleUpdateApi,
    CommentCreateApi,
)

comment_urlpatterns = [
    path(
        "articles/<int:pk>/comments/create/",
        CommentCreateApi.as_view(),
        name="comments",
    )
]

article_urlpatterns = [
    path(
        "articles/create/",
        ArticleCreateApi.as_view(),
        name="articles",
    ),
    path(
        "articles/",
        ArticleListApi.as_view(),
        name="articles",
    ),
    path(
        "articles/<int:pk>/update/",
        ArticleUpdateApi.as_view(),
        name="articles",
    ),
    path(
        "articles/<int:pk>/delete/",
        ArticleDeleteApi.as_view(),
        name="articles",
    ),
]

urlpatterns = comment_urlpatterns + article_urlpatterns
