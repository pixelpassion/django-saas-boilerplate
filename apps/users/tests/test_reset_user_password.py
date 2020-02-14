from django.utils.encoding import force_text

import pytest

from apps.core.tests.base_test_utils import (
    generate_uid_and_token,
    mock_email_backend_send_messages,
)
from apps.users.constants.messages import EXPIRED_LINK_MESSAGE

from .constants import NEW_TEST_PASSWORD, PASS_RESET_CONFIRM_URL, PASS_RESET_URL

pytestmark = pytest.mark.django_db


def test_password_reset_with_invalid_email(client, mocker):
    mocked_email_func = mock_email_backend_send_messages(mocker)

    post_data = {"email": "wrong_email@mail.com"}
    response = client.post(PASS_RESET_URL, post_data)

    assert mocked_email_func.call_count == 0
    assert response.status_code == 200


def test_password_reset_with_valid_email(user, client, mocker):
    mocked_email_func = mock_email_backend_send_messages(mocker)

    post_data = {"email": user.email}
    response = client.post(PASS_RESET_URL, post_data)

    assert response.status_code == 200
    assert mocked_email_func.call_count == 1


def test_password_set_with_valid_password(user, client):
    old_password_change_date = user.last_password_change_date
    url_kwargs = generate_uid_and_token(user)

    post_data = {
        "new_password": NEW_TEST_PASSWORD,
        "uid": force_text(url_kwargs["uuid"]),
        "token": url_kwargs["token"],
    }

    response = client.post(PASS_RESET_CONFIRM_URL, post_data, format="json")
    user.refresh_from_db()

    assert response.status_code == 200
    assert user.check_password(NEW_TEST_PASSWORD)
    assert user.last_password_change_date != old_password_change_date


def test_password_set_with_invalid_uid_and_token(user, client):
    post_data = {
        "new_password": NEW_TEST_PASSWORD,
        "uid": "invalid",
        "token": "invalid",
    }

    response = client.post(PASS_RESET_CONFIRM_URL, post_data, format="json")
    user.refresh_from_db()

    assert response.status_code == 400
    assert response.data["messages"][0] == f"non_field_errors: {EXPIRED_LINK_MESSAGE}"
    assert not user.check_password(NEW_TEST_PASSWORD)
