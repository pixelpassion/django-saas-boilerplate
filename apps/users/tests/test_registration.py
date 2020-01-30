from copy import deepcopy

import pytest

from apps.users.constants.messages import (
    BLANK_FIELD_MESSAGE,
    REQUIRED_FLAG_MESSAGE,
    UNIQUE_EMAIL_MESSAGE,
    VALID_BOOLEAN_FIELD_MESSAGE,
)
from apps.users.constants.urls_for_tests import USER_REGISTRATION_URL
from apps.users.models import User

from .constants import CORRECT_REG_DATA

pytestmark = pytest.mark.django_db


def test_normal_registration(client):
    users_before = User.objects.count()

    response = client.post(USER_REGISTRATION_URL, CORRECT_REG_DATA, format="json")
    assert response.status_code == 201
    assert User.objects.count() == users_before + 1


def test_normal_registration_returned_data(client):
    response = client.post(USER_REGISTRATION_URL, CORRECT_REG_DATA, format="json")
    assert response.status_code == 201

    user = User.objects.latest("id")

    assert set(["first_name", "last_name", "email"]) == set(
        [field for field, value in response.data.items()]
    )

    for field, value in response.data.items():
        if field != "token":
            if field == "full_name":
                assert value == user.get_full_name()
            else:
                assert getattr(user, field) == value


def test_registration_unaccepted_privacy_policy(client):
    field = "privacy_policy"
    post_data = deepcopy(CORRECT_REG_DATA)
    post_data[field] = False

    response = client.post(USER_REGISTRATION_URL, post_data, format="json")
    assert response.status_code == 400
    assert str(response.data[field][0]) == REQUIRED_FLAG_MESSAGE


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
    assert str(response.data[empty_field][0]) == error_message


def test_registration_dublicated_email(client, user):
    post_data = deepcopy(CORRECT_REG_DATA)
    post_data["email"] = user.email
    users_before = User.objects.count()

    response = client.post(USER_REGISTRATION_URL, post_data, format="json")
    assert response.status_code == 400
    assert User.objects.count() == users_before
    assert str(response.data["email"][0]) == UNIQUE_EMAIL_MESSAGE