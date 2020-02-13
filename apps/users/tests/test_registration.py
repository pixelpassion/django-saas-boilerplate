from copy import deepcopy

import pytest

from apps.core.tests.base_test_utils import (
    get_mocked_saasy_functions,
    mock_email_backend_send_messages,
)
from apps.users.constants.messages import (
    BLANK_FIELD_MESSAGE,
    REQUIRED_FLAG_MESSAGE,
    UNIQUE_EMAIL_MESSAGE,
    VALID_BOOLEAN_FIELD_MESSAGE,
)
from apps.users.models import User

from .constants import CORRECT_REG_DATA, TOKEN_VERIFY_URL, USER_REGISTRATION_URL

pytestmark = pytest.mark.django_db


def test_normal_registration(client, mocker):
    mocked_create_mail_func, mocked_send_mail_func = get_mocked_saasy_functions(mocker)
    users_before = User.objects.count()

    response = client.post(USER_REGISTRATION_URL, CORRECT_REG_DATA, format="json")
    assert response.status_code == 201
    assert User.objects.count() == users_before + 1

    assert mocked_create_mail_func.call_count == 1
    assert mocked_send_mail_func.call_count == 1


def test_normal_registration_returned_data(client, mocker):
    mock_email_backend_send_messages(mocker)
    response = client.post(USER_REGISTRATION_URL, CORRECT_REG_DATA, format="json")
    assert response.status_code == 201

    user = User.objects.latest("id")

    assert set(["first_name", "last_name", "email", "access", "refresh"]) == set(
        [field for field, value in response.data.items()]
    )

    for field, value in response.data.items():
        if field not in ["access", "refresh"]:
            if field == "full_name":
                assert value == user.get_full_name()
            else:
                assert getattr(user, field) == value

    # check access token
    response = client.post(TOKEN_VERIFY_URL, {"token": response.data["access"]})


def test_registration_unaccepted_privacy_policy(client):
    field = "privacy_policy"
    post_data = deepcopy(CORRECT_REG_DATA)
    post_data[field] = False

    response = client.post(USER_REGISTRATION_URL, post_data, format="json")
    assert response.status_code == 400
    assert response.data["messages"][0] == f"{field}: {REQUIRED_FLAG_MESSAGE}"


@pytest.mark.parametrize(
    "empty_field,error_message",
    [
        ["first_name", BLANK_FIELD_MESSAGE],
        ["last_name", BLANK_FIELD_MESSAGE],
        ["email", BLANK_FIELD_MESSAGE],
        ["password", BLANK_FIELD_MESSAGE],
        ["privacy_policy", VALID_BOOLEAN_FIELD_MESSAGE],
    ],
)
def test_registration_required_fields(client, empty_field, error_message):
    post_data = deepcopy(CORRECT_REG_DATA)
    post_data[empty_field] = ""

    response = client.post(USER_REGISTRATION_URL, post_data, format="json")
    assert response.status_code == 400
    assert response.data["messages"][0] == f"{empty_field}: {error_message}"


def test_registration_dublicated_email(client, user):
    post_data = deepcopy(CORRECT_REG_DATA)
    post_data["email"] = user.email
    users_before = User.objects.count()

    response = client.post(USER_REGISTRATION_URL, post_data, format="json")
    assert response.status_code == 400
    assert User.objects.count() == users_before
    assert response.data["messages"][0] == f"email: {UNIQUE_EMAIL_MESSAGE}"
