from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path

from rest_framework_swagger.views import get_swagger_view

from apps.core.views import WelcomePageView

schema_view = get_swagger_view(title="Django-saas-boilerplate API")


urlpatterns = (
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/v0/", include(("apps.core.urls", "core"), namespace="v0")),
    re_path(r"^django-rq/", include("django_rq.urls")),
    path("", WelcomePageView.as_view()),
)

if settings.PUBLIC_API_DOCUMENTATION:
    urlpatterns += (path("api/docs/", schema_view, name="docs"),)
