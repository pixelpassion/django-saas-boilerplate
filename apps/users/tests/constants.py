from django.urls import reverse

from apps.users.constants.url_names import (
    CHANGE_PASS_URL_NAME,
    CREATE_USER_DATA_LINK_URL_NAME,
    GENERATE_CODE_URL_NAME,
    GENERATE_TOKEN_URL_NAME,
    LOGOUT_URL_NAME,
    PASS_RESET_CONFIRM_URL_NAME,
    PASS_RESET_URL_NAME,
    TOKEN_REFRESH_URL_NAME,
    TOKEN_VERIFY_URL_NAME,
    USER_API_URL_NAME,
    USER_REGISTRATION_URL_NAME,
)

# urls
USER_REGISTRATION_URL = reverse(f"v0:{USER_REGISTRATION_URL_NAME}")
USER_API_URL = reverse(f"v0:{USER_API_URL_NAME}")
LOGOUT_URL = reverse(f"v0:{LOGOUT_URL_NAME}")
PASS_RESET_URL = reverse(f"v0:{PASS_RESET_URL_NAME}")
PASS_RESET_CONFIRM_URL = reverse(f"v0:{PASS_RESET_CONFIRM_URL_NAME}")
CHANGE_PASS_URL = reverse(f"v0:{CHANGE_PASS_URL_NAME}")
TOKEN_REFRESH_URL = reverse(f"v0:{TOKEN_REFRESH_URL_NAME}")
TOKEN_VERIFY_URL = reverse(f"v0:{TOKEN_VERIFY_URL_NAME}")
CREATE_USER_DATA_LINK_URL = reverse(f"v0:{CREATE_USER_DATA_LINK_URL_NAME}")
GENERATE_CODE_URL = reverse(f"v0:{GENERATE_CODE_URL_NAME}")
GENERATE_TOKEN_URL = reverse(f"v0:{GENERATE_TOKEN_URL_NAME}")


TEST_EMAIL = "new_user@email.com"
TEST_PASSWORD = "!TestPassword1"  # noqa
NEW_TEST_PASSWORD = "!TestPassword2"  # noqa

CORRECT_REG_DATA = {
    "first_name": "New",
    "last_name": "User",
    "email": TEST_EMAIL,
    "password": TEST_PASSWORD,
    "privacy_policy": True,
}
