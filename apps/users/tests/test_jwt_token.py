import uuid

from django.http import HttpResponse
from django.test import Client

import pytest
from rest_framework import status

from apps.users.constants.urls_for_tests import (
    REFRESH_TOKEN_URL,
    TOKEN_AUTH_URL,
    TOKEN_VERIFY_URL,
)

from .constants import TEST_PASSWORD

pytestmark = pytest.mark.django_db


def check_response_and_token(resp: HttpResponse) -> str:
    """ Checks if response and token is OK. Returns token
    """
    assert resp.status_code == status.HTTP_200_OK

    token = resp.data.get("token", None)
    assert token
    return token


def set_client_token(token: str, client: Client):
    """ Sets HTTP_AUTHORIZATION for client
    """
    client.defaults["HTTP_AUTHORIZATION"] = f"Bearer {token}"


def test_refresh_token(user, client):

    payload = {"email": user.email, "password": TEST_PASSWORD}
    response = client.post(TOKEN_AUTH_URL, payload)

    old_token = check_response_and_token(response)
    set_client_token(old_token, client)

    response = client.post(REFRESH_TOKEN_URL, {"token": old_token})

    new_token = check_response_and_token(response)

    assert old_token == new_token

    test_data = {old_token: status.HTTP_403_FORBIDDEN, new_token: status.HTTP_200_OK}

    for token, needed_status in test_data.items():
        set_client_token(token, client)
        response = client.post(TOKEN_VERIFY_URL, {"token": token})
        assert response.status_code == needed_status


def test_change_security_hash(user, client):
    payload = {"email": user.email, "password": TEST_PASSWORD}
    response = client.post(TOKEN_AUTH_URL, payload)

    token = check_response_and_token(response)

    set_client_token(token, client)

    user.security_hash = str(uuid.uuid4())
    user.save(update_fields=["security_hash"])

    response = client.post(TOKEN_VERIFY_URL, {"token": token})
    assert response.status_code == status.HTTP_403_FORBIDDEN
