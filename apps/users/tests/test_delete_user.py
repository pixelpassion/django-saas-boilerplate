import pytest

from apps.core.tests.base_test_utils import mock_email_service_function
from apps.users.models import User

from .constants import TEST_PASSWORD, TOKEN_OBTAIN_PAIR_URL, USER_API_URL

pytestmark = pytest.mark.django_db


def test_user_deletion_deleted_status(logged_in_client, user, mocker):
    mock_email_service_function(mocker, "send_account_scheduled_for_deletion_email")
    assert not user.is_deleted
    user_count_before = User.objects.count()

    response = logged_in_client.delete(USER_API_URL)
    assert response.status_code == 204
    assert User.objects.count() == user_count_before

    # test user data
    user.refresh_from_db()
    assert user.is_deleted


def test_user_deletion_send_email(logged_in_client, mocker):
    mocked_email_func = mock_email_service_function(
        mocker, "send_account_scheduled_for_deletion_email"
    )

    response = logged_in_client.delete(USER_API_URL)
    assert response.status_code == 204

    assert mocked_email_func.call_count == 1


def test_change_deleted_status_if_user_logged_in(client, user, mocker):
    mock_email_service_function(mocker, "send_account_was_recovered_email")
    user.is_deleted = True
    user.save()

    response = client.post(
        TOKEN_OBTAIN_PAIR_URL, {"email": user.email, "password": TEST_PASSWORD}
    )

    assert response.status_code == 200
    assert response.data.get("token", None)

    # test user data
    user.refresh_from_db()
    assert not user.is_deleted
    assert user.warning_sent_email == User.NO_WARNING


def test_send_email_deleted_user_logged_in(client, user, mocker):
    mocked_email_func = mock_email_service_function(
        mocker, "send_account_was_recovered_email"
    )
    user.is_deleted = True
    user.save()

    response = client.post(
        TOKEN_OBTAIN_PAIR_URL, {"email": user.email, "password": TEST_PASSWORD}
    )

    assert response.status_code == 200
    assert mocked_email_func.call_count == 1
