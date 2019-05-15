from django.contrib import admin
from django.urls import include, path
from apps.core.urls import router


urlpatterns = (
    path("admin/", admin.site.urls),
    path("api/v0/", include((router.urls, "apps.core"), namespace="v0")),
)
