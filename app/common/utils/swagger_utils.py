from drf_spectacular.utils import OpenApiParameter

limit_offset_parameters = [
    OpenApiParameter(
        name="limit",
        description="limit",
        required=False,
        type=str,
    ),
    OpenApiParameter(
        name="offset",
        description="offset",
        required=False,
        type=str,
    ),
]
