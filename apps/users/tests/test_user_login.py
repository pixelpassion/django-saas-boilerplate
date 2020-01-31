import pytest

from apps.users.constants.urls_for_tests import TOKEN_AUTH_URL

from .constants import TEST_EMAIL, TEST_PASSWORD

pytestmark = pytest.mark.django_db


def test_correct_login(user, client):
    payload = {"email": user.email, "password": TEST_PASSWORD}

    response = client.post(TOKEN_AUTH_URL, payload)

    assert response.status_code == 200
    assert response.data["token"]


@pytest.mark.parametrize(
    "payload",
    [
        {"email": TEST_EMAIL, "password": "TEST_PASSWORD"},
        {"email": "asd@Asd.asd", "password": TEST_PASSWORD},
        {"email": "asd@Asd.asd", "password": "TEST_PASSWORD"},
        {"username": TEST_EMAIL, "password": TEST_PASSWORD},
    ],
)
def test_incorrect_login(user, client, payload):
    response = client.post(TOKEN_AUTH_URL, payload)

    assert response.status_code != 200

    assert not response.data.get("token", None)


def test_correct_login_inactive_user(user, client):
    user.is_active = False
    user.save()
    payload = {"email": user.email, "password": TEST_PASSWORD}

    response = client.post(TOKEN_AUTH_URL, payload)

    assert response.status_code == 400
    assert (
        str(response.data["non_field_errors"][0])
        == "Unable to log in with provided credentials."
    )
    assert not response.data.get("token", None)


def test_login_username(user, client):
    response = client.post(
        TOKEN_AUTH_URL, {"username": user.username, "password": TEST_PASSWORD}
    )

    assert response.status_code == 400
    assert not response.data.get("token", None)


def test_login_returned_data(client, user):
    payload = {"email": user.email, "password": TEST_PASSWORD}
    response = client.post(TOKEN_AUTH_URL, payload)
    assert response.status_code == 200

    assert set(["email", "token", "first_name", "last_name"]) == set(
        [field for field, value in response.data.items()]
    )

    for field, value in response.data.items():
        if field != "token":
            if field == "full_name":
                assert value == user.get_full_name()
            else:
                assert getattr(user, field) == value
