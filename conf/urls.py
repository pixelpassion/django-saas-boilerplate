from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter


router = DefaultRouter()


urlpatterns = (
    path("admin/", admin.site.urls),
    path("api/v0/", include(router.urls)),
)
