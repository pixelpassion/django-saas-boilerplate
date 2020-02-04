import uuid

import pytest

from apps.users.constants.messages import INVALID_ACCESS_TOKEN_MESSAGE

from .constants import (
    TEST_PASSWORD,
    TOKEN_OBTAIN_PAIR_URL,
    TOKEN_VERIFY_URL,
    USER_API_URL,
)

pytestmark = pytest.mark.django_db


def test_change_security_hash(user, client):
    payload = {"email": user.email, "password": TEST_PASSWORD}
    response = client.post(TOKEN_OBTAIN_PAIR_URL, payload)

    assert response.status_code == 200

    access = response.data.get("access", None)
    refresh = response.data.get("refresh", None)
    assert access
    assert refresh

    user.security_hash = str(uuid.uuid4())
    user.save(update_fields=["security_hash"])

    response = client.post(TOKEN_VERIFY_URL, {"token": access})
    assert response.status_code == 400
    assert (
        response.data["messages"][0]
        == f"non_field_errors: {INVALID_ACCESS_TOKEN_MESSAGE}"
    )

    client.defaults["HTTP_AUTHORIZATION"] = f"Bearer {access}"
    assert client.get(USER_API_URL).status_code == 401  # url for auth users
