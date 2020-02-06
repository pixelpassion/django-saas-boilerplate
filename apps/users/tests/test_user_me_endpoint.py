from django.conf import settings

import pytest

from .constants import USER_API_URL

pytestmark = pytest.mark.django_db

returned_data_fields = ["first_name", "last_name", "email"]
TEST_ERROR_MESSAGE = "value for {} field is different"


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
