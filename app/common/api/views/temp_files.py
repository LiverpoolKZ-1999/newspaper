from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from app.common.api.mixins import ServiceExceptionHandlerMixin
from app.common.services.temp_file_services import temporary_file_create


class TemporaryFileUploadApi(ServiceExceptionHandlerMixin, APIView):
    """
    Endpoint to Upload Job contract file

    params:
     * file - FileField
    """

    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)

    class InnerSerializer(serializers.Serializer):
        file = serializers.FileField()

        class Meta:
            ref_name = "TemporaryFileUploadInputSerializer"

    class OutputSerializer(serializers.Serializer):
        file_uuid = serializers.UUIDField()
        filename = serializers.CharField()
        file = serializers.FileField()

        class Meta:
            ref_name = "TemporaryFileUploadOutputSerializer"

    @extend_schema(
        tags=["TemporaryFile"],
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {"file": {"type": "string", "format": "binary"}},
            }
        },
    )
    def post(self, request):
        serializer = self.InnerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = temporary_file_create(file=serializer.validated_data["file"])

        return Response(
            data=self.OutputSerializer(instance).data, status=HTTP_201_CREATED
        )
