from django.urls import reverse

from .url_names import REST_LOGIN_URL_NAME, USER_API_URL_NAME

USER_API_URL = reverse(f"v0:{USER_API_URL_NAME}")
REST_LOGIN_URL = reverse(REST_LOGIN_URL_NAME)
