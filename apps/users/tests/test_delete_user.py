from datetime import datetime

import pytest

from apps.users.constants.template_names import ACCOUNT_WAS_DELETED_EMAIL_TEMPLATE
from apps.users.models import User

from .base_test_utils import mock_users_email_service_function
from .constants import GENERATE_CODE_URL, TEST_PASSWORD, USER_API_URL

pytestmark = pytest.mark.django_db


def test_user_deletion_deleted_status(logged_in_client, user, mocker):
    mock_users_email_service_function(
        mocker, "send_account_scheduled_for_deletion_email"
    )
    assert not user.is_deleted
    user_count_before = User.objects.count()

    response = logged_in_client.delete(USER_API_URL)
    assert response.status_code == 204
    assert User.objects.count() == user_count_before

    # test user data
    user.refresh_from_db()
    assert user.is_deleted


def test_user_deletion_if_retention_in_days_is_zero(
    logged_in_client, user, mocker, settings
):
    settings.ACCOUNT_DELETION_RETENTION_IN_DAYS = 0
    mock_users_email_service_function(mocker, "send_account_was_deleted_email")
    assert not user.is_deleted
    user_count_before = User.objects.count()

    response = logged_in_client.delete(USER_API_URL)

    assert response.status_code == 204
    assert User.objects.count() == user_count_before - 1


def test_user_deletion_if_retention_in_days_is_zero_send_mail(
    logged_in_client, user, mocker, settings
):
    settings.ACCOUNT_DELETION_RETENTION_IN_DAYS = 0
    mocked_email_func = mock_users_email_service_function(mocker, "_send_message")
    assert not user.is_deleted

    response = logged_in_client.delete(USER_API_URL)
    assert response.status_code == 204

    # test mail
    assert mocked_email_func.call_count == 2
    call_data = mocked_email_func.call_args[0]
    assert call_data[0] == user.email
    assert call_data[1] == ACCOUNT_WAS_DELETED_EMAIL_TEMPLATE


def test_user_deletion_send_email(logged_in_client, mocker):
    mocked_email_func = mock_users_email_service_function(
        mocker, "send_account_scheduled_for_deletion_email"
    )

    response = logged_in_client.delete(USER_API_URL)
    assert response.status_code == 204

    assert mocked_email_func.call_count == 1


def test_change_deleted_status_if_user_logged_in(client, user, mocker):
    mock_users_email_service_function(mocker, "send_account_was_recovered_email")
    user.is_deleted = True
    user.last_login = datetime.today()
    user.save()

    response = client.post(
        GENERATE_CODE_URL, {"email": user.email, "password": TEST_PASSWORD}
    )
    assert response.status_code == 200

    # test user data
    user.refresh_from_db()
    assert not user.is_deleted


def test_send_email_deleted_user_logged_in(client, user, mocker):
    mocked_email_func = mock_users_email_service_function(
        mocker, "send_account_was_recovered_email"
    )
    user.is_deleted = True
    user.last_login = datetime.today()
    user.save()

    response = client.post(
        GENERATE_CODE_URL, {"email": user.email, "password": TEST_PASSWORD}
    )

    assert response.status_code == 200
    assert mocked_email_func.call_count == 1
