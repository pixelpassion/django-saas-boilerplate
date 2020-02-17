from django.urls import include, path

from rest_framework.routers import DefaultRouter

from apps.users.constants.url_names import (
    GENERATE_CODE_URL_NAME,
    GENERATE_TOKEN_URL_NAME,
)
from apps.users.views import MyTokenObtainPairView, MyTokenObtainPairViewWithMFA

router = DefaultRouter()

urlpatterns = [
    path("users/", include("apps.users.urls")),
    path("auth/login/", MyTokenObtainPairView.as_view(), name=GENERATE_CODE_URL_NAME),
    path(
        "auth/login/code/",
        MyTokenObtainPairViewWithMFA.as_view(),
        name=GENERATE_TOKEN_URL_NAME,
    ),
    path("auth/", include("trench.urls")),
]
urlpatterns += router.urls
