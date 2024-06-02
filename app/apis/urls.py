from django.urls import include, re_path

urlpatterns = [
    re_path("v1/", include(("app.auth_.api.urls", "auth_"), namespace="v1")),
]
