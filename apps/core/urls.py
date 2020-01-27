from django.conf import settings
from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import TestApiView

router = DefaultRouter()
urlpatterns = []

# TODO: remove this test handler as soon as we have actual views to test against
if settings.ENV in ["test", "local"]:
    urlpatterns += [
        path("handler-test/", TestApiView.as_view(), name="handler-test-url")
    ]

urlpatterns += router.urls
