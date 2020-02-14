import uuid

import pytest

from apps.users.constants.messages import INVALID_TOKEN_MESSAGE

from .constants import (
    GENERATE_CODE_URL,
    TEST_PASSWORD,
    TOKEN_REFRESH_URL,
    TOKEN_VERIFY_URL,
    USER_API_URL,
)

pytestmark = pytest.mark.django_db


def test_change_security_hash(user, client):
    # get valid token
    payload = {"email": user.email, "password": TEST_PASSWORD}
    response = client.post(GENERATE_CODE_URL, payload)
    assert response.status_code == 200
    access = response.data.get("access")
    refresh = response.data.get("refresh")
    assert access
    assert refresh

    # change user security hash
    user.security_hash = uuid.uuid4()
    user.save(update_fields=["security_hash"])

    # verify token
    response = client.post(TOKEN_VERIFY_URL, {"token": access})
    assert response.status_code == 400
    assert response.data["messages"][0] == f"non_field_errors: {INVALID_TOKEN_MESSAGE}"

    # check if the user has access to the url for auth users
    client.defaults["HTTP_AUTHORIZATION"] = f"Bearer {access}"
    assert client.get(USER_API_URL).status_code == 401  # url for auth users


def test_refresh_token_after_security_hash_change(user, client):
    # get valid token
    payload = {"email": user.email, "password": TEST_PASSWORD}
    response = client.post(GENERATE_CODE_URL, payload)
    assert response.status_code == 200
    access = response.data.get("access")
    refresh = response.data.get("refresh")
    assert access
    assert refresh

    # set token to the header and chenage security hash
    client.defaults["HTTP_AUTHORIZATION"] = f"Bearer {access}"
    user.security_hash = uuid.uuid4()
    user.save(update_fields=["security_hash"])

    # verify token
    response = client.post(TOKEN_VERIFY_URL, {"token": access})
    assert response.status_code == 400
    assert response.data["messages"][0] == f"non_field_errors: {INVALID_TOKEN_MESSAGE}"

    # refresh token
    response = client.post(TOKEN_REFRESH_URL, {"refresh": refresh})
    assert response.status_code == 400
    assert response.data["messages"][0] == f"non_field_errors: {INVALID_TOKEN_MESSAGE}"
