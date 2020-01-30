from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = (
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/v0/", include(("apps.core.urls", "core"), namespace="v0")),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    re_path(r"^django-rq/", include("django_rq.urls")),
)
