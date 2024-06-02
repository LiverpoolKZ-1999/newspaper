from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
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
    path(route="api/auth/", view=include(arg="app.auth_.api.urls")),
)
