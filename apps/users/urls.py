from django.urls import path

from rest_auth.views import (
    LogoutView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from rest_framework_jwt.views import (
    ObtainJSONWebToken,
    refresh_jwt_token,
    verify_jwt_token,
)

from .constants.url_names import (
    CHANGE_PASS_URL_NAME,
    LOGOUT_URL_NAME,
    PASS_RESET_CONFIRM_URL_NAME,
    PASS_RESET_URL_NAME,
    REFRESH_TOKEN_URL_NAME,
    TOKEN_AUTH_URL_NAME,
    TOKEN_VERIFY_URL_NAME,
    USER_API_URL_NAME,
    USER_REGISTRATION_URL_NAME,
)
from .views import UserApiView, UserRegistrationView

urlpatterns = [
    path("", UserRegistrationView.as_view(), name=USER_REGISTRATION_URL_NAME),
    path("api-token-auth/", ObtainJSONWebToken.as_view(), name=TOKEN_AUTH_URL_NAME),
    path("api-token-refresh/", refresh_jwt_token, name=REFRESH_TOKEN_URL_NAME),
    path("api-token-verify/", verify_jwt_token, name=TOKEN_VERIFY_URL_NAME),
    path("logout/", LogoutView.as_view(), name=LOGOUT_URL_NAME),
    path("password/change/", PasswordChangeView.as_view(), name=CHANGE_PASS_URL_NAME),
    path("password/reset/", PasswordResetView.as_view(), name=PASS_RESET_URL_NAME),
    path(
        "password/reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name=PASS_RESET_CONFIRM_URL_NAME,
    ),
    path("me/", UserApiView.as_view({"get": "retrieve"}), name=USER_API_URL_NAME),
]
