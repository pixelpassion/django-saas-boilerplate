from django.urls import path

from rest_auth.views import (
    LogoutView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
)

from .constants.url_names import (
    CHANGE_PASS_URL_NAME,
    CREATE_USER_DATA_LINK_URL_NAME,
    GET_USER_DATA_URL_NAME,
    LOGOUT_URL_NAME,
    PASS_RESET_CONFIRM_URL_NAME,
    PASS_RESET_URL_NAME,
    TOKEN_REFRESH_URL_NAME,
    TOKEN_VERIFY_URL_NAME,
    USER_API_URL_NAME,
    USER_REGISTRATION_URL_NAME,
)
from .views import (
    MyTokenRefreshView,
    MyTokenVerifyView,
    UserAccountDataView,
    UserApiView,
    UserRegistrationView,
)

urlpatterns = [
    path("", UserRegistrationView.as_view(), name=USER_REGISTRATION_URL_NAME),
    path(
        "api/token/refresh/", MyTokenRefreshView.as_view(), name=TOKEN_REFRESH_URL_NAME
    ),
    path("api/token/verify/", MyTokenVerifyView.as_view(), name=TOKEN_VERIFY_URL_NAME),
    path("logout/", LogoutView.as_view(), name=LOGOUT_URL_NAME),
    path("password/change/", PasswordChangeView.as_view(), name=CHANGE_PASS_URL_NAME),
    path("password/reset/", PasswordResetView.as_view(), name=PASS_RESET_URL_NAME),
    path(
        "password/reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name=PASS_RESET_CONFIRM_URL_NAME,
    ),
    path(
        "me/",
        UserApiView.as_view(
            {"get": "retrieve", "patch": "update", "delete": "perform_destroy"}
        ),
        name=USER_API_URL_NAME,
    ),
    path(
        "me/account-data/",
        UserAccountDataView.as_view(),
        name=CREATE_USER_DATA_LINK_URL_NAME,
    ),
    path(
        "me/account-data/<str:account_info_link>/",
        UserAccountDataView.as_view(),
        name=GET_USER_DATA_URL_NAME,
    ),
]
