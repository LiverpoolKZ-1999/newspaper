from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from app.common.api.mixins import ServiceExceptionHandlerMixin
from app.core.models import Article
from app.core.services import create_comment


class CommentCreateApi(ServiceExceptionHandlerMixin, APIView):
    """
    Create comment
    """

    permission_classes = (AllowAny,)

    class InputSerializer(serializers.Serializer):
        text = serializers.CharField()

        class Meta:
            ref_name = "CommentCreateInputSerializer"

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        text = serializers.CharField()

        class Meta:
            ref_name = "CommentCreateOutputSerializer"

    @extend_schema(
        tags=["Comments"],
        responses=OutputSerializer,
        request=InputSerializer,
    )
    def post(self, request, pk):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        article = get_object_or_404(Article, pk=pk)
        validated_data = serializer.validated_data
        result = create_comment(
            name=validated_data["name"],
            article=article,
        )
        return Response(
            self.OutputSerializer(result).data, status=status.HTTP_201_CREATED
        )
