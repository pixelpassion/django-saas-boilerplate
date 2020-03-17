from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from apps.core.views import WelcomePageView

schema_view = get_schema_view(
    openapi.Info(
        title="Django-saas-boilerplate API",
        default_version="v0",
        description="Django-saas-boilerplate API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = (
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/v0/", include(("apps.core.urls", "core"), namespace="v0")),
    re_path(r"^django-rq/", include("django_rq.urls")),
    path("", WelcomePageView.as_view()),
)

if settings.PUBLIC_API_DOCUMENTATION or settings.DEBUG:
    urlpatterns += (
        re_path(
            r"^docs/$", schema_view.with_ui("swagger", cache_timeout=0), name="docs"
        ),
    )
