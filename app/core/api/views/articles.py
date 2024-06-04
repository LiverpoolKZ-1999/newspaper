from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.common.api.mixins import ServiceExceptionHandlerMixin
from app.common.models import TemporaryFile
from app.core.models import Article, Author, Comment, Tag, Topic
from app.core.services import (
    article_create,
    article_delete,
    article_list,
    article_update,
)


class ArticleCreateApi(ServiceExceptionHandlerMixin, APIView):
    """
    Article create
    """

    permission_classes = [
        IsAuthenticated,
    ]

    class InputSerializer(serializers.Serializer):
        class ArticleBlockSerializer(serializers.Serializer):
            order = serializers.IntegerField()
            text = serializers.CharField(default=None)
            background_text = serializers.CharField(default=None)
            video_url = serializers.CharField(default=None)
            image = serializers.PrimaryKeyRelatedField(
                queryset=TemporaryFile.objects.all(), default=None
            )
            text_tag = serializers.CharField(default=None)
            block_divider = serializers.BooleanField(default=False)

            class Meta:
                ref_name = "ArticleCreateInputArticleBlockSerializer"

        name = serializers.CharField()
        short_description = serializers.CharField()
        author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
        topic = serializers.PrimaryKeyRelatedField(queryset=Topic.objects.all())
        tags = serializers.ListSerializer(
            child=serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all()),
            default=[],
        )
        blocks = ArticleBlockSerializer(many=True)

        class Meta:
            ref_name = "ArticleCreateInputSerializer"

    class OutputSerializer(serializers.Serializer):
        class ArticleBlockSerializer(serializers.Serializer):
            id = serializers.IntegerField()
            order = serializers.IntegerField()
            text = serializers.CharField(default=None)
            background_text = serializers.CharField(default=None)
            video_url = serializers.CharField(default=None)
            image = serializers.PrimaryKeyRelatedField(
                queryset=TemporaryFile.objects.all(), default=None
            )
            text_tag = serializers.CharField(default=None)
            block_divider = serializers.BooleanField(default=False)

            class Meta:
                ref_name = "ArticleCreateOutputArticleBlockSerializer"

        class AuthorSerializer(serializers.ModelSerializer):
            class Meta:
                model = Author
                fields = ("id", "first_name", "last_name", "bio", "avatar")
                ref_name = "ArticleCreateOutputAuthorSerializer"

        class TopicSerializer(serializers.ModelSerializer):
            class Meta:
                model = Topic
                fields = ("id", "name")
                ref_name = "ArticleCreateOutputTopicSerializer"

        class TagSerializer(serializers.ModelSerializer):
            class Meta:
                model = Tag
                fields = ("id", "name")
                ref_name = "ArticleCreateOutputTagSerializer"

        class CommentSerializer(serializers.ModelSerializer):
            class Meta:
                model = Comment
                fields = ("id", "created_at", "text")
                ref_name = "ArticleCreateOutputCommentSerializer"

        created_at = serializers.DateTimeField()
        id = serializers.IntegerField()
        view_count = serializers.IntegerField()
        name = serializers.CharField()
        short_description = serializers.CharField()
        author = AuthorSerializer()
        topic = TopicSerializer()
        tags = TagSerializer(many=True)
        blocks = ArticleBlockSerializer(many=True)
        comments = CommentSerializer(many=True)

        class Meta:
            ref_name = "ArticleCreateOutputSerializer"

    @extend_schema(
        tags=["Articles"],
        responses=OutputSerializer,
        request=InputSerializer,
        description="Article create",
    )
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        result = article_create(
            name=validated_data["name"],
            short_description=validated_data["short_description"],
            author=validated_data["author"],
            topic=validated_data["topic"],
            blocks=validated_data["blocks"],
            tags=validated_data["tags"],
        )
        return Response(
            self.OutputSerializer(result).data, status=status.HTTP_201_CREATED
        )


class ArticleUpdateApi(ServiceExceptionHandlerMixin, APIView):
    """
    Article update
    """

    permission_classes = [
        IsAuthenticated,
    ]

    class InputSerializer(serializers.Serializer):
        class ArticleBlockSerializer(serializers.Serializer):
            order = serializers.IntegerField()
            text = serializers.CharField(default=None)
            background_text = serializers.CharField(default=None)
            video_url = serializers.CharField(default=None)
            image = serializers.PrimaryKeyRelatedField(
                queryset=TemporaryFile.objects.all(), default=None
            )
            text_tag = serializers.CharField(default=None)
            block_divider = serializers.BooleanField(default=False)

            class Meta:
                ref_name = "ArticleUpdateInputArticleBlockSerializer"

        name = serializers.CharField(required=False)
        short_description = serializers.CharField(required=False)
        author = serializers.PrimaryKeyRelatedField(
            queryset=Author.objects.all(), required=False
        )
        topic = serializers.PrimaryKeyRelatedField(
            queryset=Topic.objects.all(), required=False
        )
        tags = serializers.ListSerializer(
            child=serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all()),
            required=False,
        )
        blocks = ArticleBlockSerializer(many=True, required=False)

        class Meta:
            ref_name = "ArticleUpdateInputSerializer"

    @extend_schema(
        tags=["Articles"],
        responses=ArticleCreateApi.OutputSerializer,
        request=InputSerializer,
        description="Article update",
    )
    def patch(self, request, pk):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        article = get_object_or_404(Article, pk=pk)
        article_blocks = serializer.validated_data.pop("blocks")
        article = article_update(
            article=article,
            article_data=serializer.validated_data,
            article_blocks=article_blocks,
        )
        return Response(
            ArticleCreateApi.OutputSerializer(article).data, status=status.HTTP_200_OK
        )


class ArticleListApi(ServiceExceptionHandlerMixin, APIView):
    """
    Article list API
    """

    permission_classes = [
        IsAuthenticated,
    ]

    @extend_schema(
        tags=["Articles"],
        responses=ArticleCreateApi.OutputSerializer,
        description="Article list",
    )
    def get(self, request):
        article = article_list()
        return Response(
            ArticleCreateApi.OutputSerializer(article).data, status=status.HTTP_200_OK
        )


class ArticleDeleteApi(ServiceExceptionHandlerMixin, APIView):
    """
    Article delete API
    """

    permission_classes = [
        IsAuthenticated,
    ]

    @extend_schema(
        tags=["Articles"],
        responses=ArticleCreateApi.OutputSerializer,
        description="Article delete",
    )
    def delete(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        article_delete(article=article)
        return Response(status=status.HTTP_204_NO_CONTENT)
