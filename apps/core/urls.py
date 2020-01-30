from django.urls import include, path

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [path("users/", include("apps.users.urls"))]
urlpatterns += router.urls
