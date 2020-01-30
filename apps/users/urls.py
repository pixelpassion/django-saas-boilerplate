from django.urls import path

from .constants.url_names import USER_API_URL_NAME
from .views import UserApiView

urlpatterns = [
    path("me/", UserApiView.as_view({"get": "retrieve"}), name=USER_API_URL_NAME)
]
