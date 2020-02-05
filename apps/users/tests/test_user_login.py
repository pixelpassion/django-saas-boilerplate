import pytest

from .constants import TEST_EMAIL, TEST_PASSWORD, TOKEN_OBTAIN_PAIR_URL

pytestmark = pytest.mark.django_db


def test_correct_login(user, client):
    payload = {"email": user.email, "password": TEST_PASSWORD}

    response = client.post(TOKEN_OBTAIN_PAIR_URL, payload)

    assert response.status_code == 200
    assert response.data["refresh"]
    assert response.data["access"]


@pytest.mark.parametrize(
    "payload",
    [
        {"email": TEST_EMAIL, "password": "TEST_PASSWORD"},
        {"email": "asd@Asd.asd", "password": TEST_PASSWORD},
        {"email": "asd@Asd.asd", "password": "TEST_PASSWORD"},
    ],
)
def test_incorrect_login(user, client, payload):
    response = client.post(TOKEN_OBTAIN_PAIR_URL, payload)

    assert response.status_code != 200
    assert (
        response.data["messages"][0]
        == "No active account found with the given credentials"
    )


def test_correct_login_inactive_user(user, client):
    user.is_active = False
    user.save()
    payload = {"email": user.email, "password": TEST_PASSWORD}

    response = client.post(TOKEN_OBTAIN_PAIR_URL, payload)

    assert response.status_code == 401
    assert (
        response.data["messages"][0]
        == "No active account found with the given credentials"
    )


def test_login_username(user, client):
    response = client.post(
        TOKEN_OBTAIN_PAIR_URL, {"username": user.username, "password": TEST_PASSWORD}
    )

    assert response.status_code == 400
    assert response.data["messages"][0] == "email: This field is required."


def test_login_returned_data(client, user):
    payload = {"email": user.email, "password": TEST_PASSWORD}
    response = client.post(TOKEN_OBTAIN_PAIR_URL, payload)
    assert response.status_code == 200

    assert set(["refresh", "access"]) == set(
        [field for field, value in response.data.items()]
    )
