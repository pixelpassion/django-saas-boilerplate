import pytest
from jwt.exceptions import DecodeError
from rest_framework_jwt.compat import get_username
from rest_framework_jwt.utils import jwt_encode_handler

from apps.users.custom_jwt import custom_jwt_decode_handler, custom_jwt_payload_handler

pytestmark = pytest.mark.django_db


def test_custom_jwt_payload_handler(user):
    payload = custom_jwt_payload_handler(user)

    assert isinstance(payload, dict)
    assert len(payload) == 5

    assert payload["user_id"] == user.pk
    assert payload["username"] == get_username(user)
    assert payload["security_hash"] == str(user.security_hash)
    assert "exp" in payload


def test_custom_jwt_decode_handler(user):
    payload = custom_jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    decoded_payload = custom_jwt_decode_handler(token)

    assert decoded_payload == payload


def test_custom_jwt_decode_handler_fake_payload():
    payload = {
        "user_id": 12345,
        "username": "fake_user@email.com",
        "exp": "fake_data",
        "orig_iat": "fake_iat",
        "security_hash": "fake_hash",
    }
    token = jwt_encode_handler(payload)
    with pytest.raises(DecodeError):
        custom_jwt_decode_handler(token)


def test_custom_jwt_decode_handler_fake_token():
    with pytest.raises(DecodeError):
        custom_jwt_decode_handler("fake_token")
