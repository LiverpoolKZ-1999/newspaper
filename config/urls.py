from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckViewSet(APIView):
    permission_classes = [
        AllowAny,
    ]

    def get(self, request):
        return Response(data={"message": "ok"})


urlpatterns = i18n_patterns(
    # path(route='admin/', view=admin.site.urls),
)
urlpatterns += (
    path(route="health-check/", view=HealthCheckViewSet.as_view()),
    path(route="api/admin/", view=admin.site.urls),
    path(route="api/", view=include(arg="app.apis.urls")),
)

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += [
        path(
            "api/v1/schema/",
            SpectacularAPIView.as_view(api_version="v1"),
            name="schema_v1",
        ),
        path(
            "",
            SpectacularSwaggerView.as_view(url_name="schema_v1"),
            name="swagger-ui",
        ),
        path(
            "api/v1/schema/redoc/",
            SpectacularRedocView.as_view(url_name="schema_v1"),
            name="redoc",
        ),
    ]

    urlpatterns += (path(route="silk/", view=include(arg="silk.urls")),)

    urlpatterns += tuple(
        static(prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    )
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
