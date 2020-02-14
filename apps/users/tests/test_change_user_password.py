import pytest

from .constants import CHANGE_PASS_URL, NEW_TEST_PASSWORD, TEST_PASSWORD

pytestmark = pytest.mark.django_db


def test_change_password_page_anon_user(client):
    response = client.post(CHANGE_PASS_URL)
    assert response.status_code == 401


@pytest.mark.parametrize(
    "payload",
    [
        {"old_password": "123123", "new_password": "123123"},
        {"old_password": "", "new_password": ""},
        {"old_password": "newpass2", "new_password": "newpass20"},
        {"old_password": "dummy", "new_password": ""},
        {"old_password": "dummy", "new_password": NEW_TEST_PASSWORD},
    ],
)
def test_change_password_invalid_data(user, logged_in_client, payload):
    response = logged_in_client.post(
        CHANGE_PASS_URL, payload, content_type="application/json"
    )

    user.refresh_from_db()
    assert response.status_code == 400
    assert not user.check_password(NEW_TEST_PASSWORD)


def test_change_password_valid_data(user, logged_in_client):
    old_password_change_date = user.last_password_change_date
    payload = {"old_password": TEST_PASSWORD, "new_password": NEW_TEST_PASSWORD}
    response = logged_in_client.post(
        CHANGE_PASS_URL, payload, content_type="application/json"
    )
    user.refresh_from_db()
    assert response.status_code == 200
    assert user.check_password(NEW_TEST_PASSWORD)
    assert user.last_password_change_date != old_password_change_date
