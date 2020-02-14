from copy import deepcopy

from django.conf import settings

import pytest

from .constants import USER_API_URL

pytestmark = pytest.mark.django_db

returned_data_fields = ["first_name", "last_name", "email", "last_password_change_date"]
TEST_ERROR_MESSAGE = "value for {} field is different"


pytestmark = pytest.mark.django_db

returned_data_fields = ["first_name", "last_name", "email"]
CORRECT_PATCH_DATA = {"first_name": "Updated", "last_name": "Name"}
TEST_ERROR_MESSAGE = "value for {} field is different"


def test_cant_update_user_email_and_username(logged_in_client, user):
    """
    Test user.email and username updating
    """
    new_email = "updated_email@mail.com"
    old_email = user.email
    assert new_email != old_email

    response = logged_in_client.patch(
        USER_API_URL, {"email": new_email}, content_type="application/json"
    )
    assert response.status_code == 200
    user.refresh_from_db()
    assert user.email == old_email
    assert user.username == old_email


def test_user_current_user_can_update(logged_in_client, user):
    """
    Test user update.
    """
    response = logged_in_client.patch(
        USER_API_URL, CORRECT_PATCH_DATA, content_type="application/json"
    )
    assert response.status_code == 200
    user.refresh_from_db()
    for field in returned_data_fields:
        response_data = response.data[field]
        error_message = TEST_ERROR_MESSAGE.format(field)
        if field != "email":
            assert response_data == CORRECT_PATCH_DATA[field], error_message
        assert response_data == getattr(user, field), error_message


@pytest.mark.parametrize("deleted_field", ["first_name", "last_name"])
def test_user_update_required_fields(logged_in_client, deleted_field):
    patch_data = deepcopy(CORRECT_PATCH_DATA)
    del patch_data[deleted_field]

    response = logged_in_client.patch(
        USER_API_URL, patch_data, content_type="application/json"
    )
    assert response.status_code == 200


def test_user_current_user_info_no_auth(client):
    """
    Test current user info without login.
    """
    response = client.get(USER_API_URL)
    assert response.status_code == 401


def test_user_current_user_info_auth(logged_in_client, user):
    """
    Test current user info.
    """
    response = logged_in_client.get(USER_API_URL)
    assert response.status_code == 200
    for field in returned_data_fields:
        error_message = TEST_ERROR_MESSAGE.format(field)
        if field == "last_password_change_date":
            assert response.data[field]
        else:
            assert response.data[field] == getattr(user, field), error_message


def test_get_admin_url_user_is_staff(logged_in_client, user):
    user.is_staff = True
    user.save()

    response = logged_in_client.get(USER_API_URL)
    assert response.status_code == 200

    assert response.data["admin_url"] == settings.ADMIN_URL


def test_get_admin_url_user_is_superuser(logged_in_client, user):
    user.is_superuser = True
    user.save()

    response = logged_in_client.get(USER_API_URL)
    assert response.status_code == 200

    assert response.data["admin_url"] == settings.ADMIN_URL


def test_get_admin_url_user_is_superuser_is_staff(logged_in_client, user):
    user.is_superuser = True
    user.is_staff = True
    user.save()

    response = logged_in_client.get(USER_API_URL)
    assert response.status_code == 200

    assert response.data["admin_url"] == settings.ADMIN_URL


def test_get_admin_url_user_is_not_staff(logged_in_client, user):
    response = logged_in_client.get(USER_API_URL)
    assert response.status_code == 200

    assert response.data["admin_url"] is None


def test_get_admin_url_user_is_not_superuser(logged_in_client, user):
    response = logged_in_client.get(USER_API_URL)
    assert response.status_code == 200

    assert response.data["admin_url"] is None
