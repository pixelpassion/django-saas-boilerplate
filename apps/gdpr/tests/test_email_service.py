from django.conf import settings

import pytest

from apps.core.tests.base_test_utils import mock_email_service_function
from apps.gdpr.constants import (
    ACCOUNT_WAS_DELETED_EMAIL_TEMPLATE,
    ACCOUNT_WAS_RECOVERED_EMAIL_TEMPLATE,
    INACTIVE_ACCOUNT_DELETION_DONE_TEMPLATE,
    INACTIVE_ACCOUNT_DELETION_WARNING_TEMPLATE,
    USER_ACCOUNT_VERIFICATION_EMAIL_TEMPLATE,
    USER_PASSWORD_RESET_EMAIL_TEMPLATE,
)
from apps.gdpr.email_service import SaasyEmailService

pytestmark = pytest.mark.django_db

email_service = SaasyEmailService()


def test_send_account_was_deleted_email(user, mocker):
    mocked_email_func = mock_email_service_function(mocker, "_send_message")

    email_service.send_account_was_deleted_email(user)
    assert mocked_email_func.call_count == 1

    call_data = mocked_email_func.call_args[0]
    assert call_data[0] == user.email
    assert call_data[1] == ACCOUNT_WAS_DELETED_EMAIL_TEMPLATE
    assert call_data[2] == {
        "LOGIN_URL": f"{settings.PUBLIC_URL}/login",
        "FROM_EMAIL": settings.INACTIVE_ACCOUNT_DELETION_BCC_EMAIL,
    }


def test_send_account_was_deleted_email_if_deletion_bcc_email_is_none(
    user, mocker, settings
):
    settings.INACTIVE_ACCOUNT_DELETION_BCC_EMAIL = None
    mocked_email_func = mock_email_service_function(mocker, "_send_message")

    email_service.send_account_was_deleted_email(user)
    assert mocked_email_func.call_count == 0


def test_send_account_was_recovered_email(user, mocker):
    mocked_email_func = mock_email_service_function(mocker, "_send_message")

    email_service.send_account_was_recovered_email(user)
    assert mocked_email_func.call_count == 1

    call_data = mocked_email_func.call_args[0]
    assert call_data[0] == user.email
    assert call_data[1] == ACCOUNT_WAS_RECOVERED_EMAIL_TEMPLATE


def test_send_warning_about_upcoming_account_deletion(user, mocker):
    mocked_email_func = mock_email_service_function(mocker, "_send_message")

    weeks = 5
    email_service.send_warning_about_upcoming_account_deletion(user, weeks)

    assert mocked_email_func.call_count == 1

    call_data = mocked_email_func.call_args[0]
    assert call_data[0] == user.email
    assert call_data[1] == INACTIVE_ACCOUNT_DELETION_WARNING_TEMPLATE
    assert call_data[2] == {
        "WEEKS_LEFT": weeks,
        "LOGIN_URL": f"{settings.PUBLIC_URL}/login",
        "FROM_EMAIL": settings.INACTIVE_ACCOUNT_WARNING_BCC_EMAIL,
    }


def test_send_warning_about_upcoming_account_deletion_if_warning_bcc_email_is_none(
    user, mocker, settings
):
    settings.INACTIVE_ACCOUNT_WARNING_BCC_EMAIL = None
    mocked_email_func = mock_email_service_function(mocker, "_send_message")

    weeks = 5
    email_service.send_warning_about_upcoming_account_deletion(user, weeks)

    assert mocked_email_func.call_count == 0


def test_send_inactive_account_was_deleted_email(user, mocker):
    mocked_email_func = mock_email_service_function(mocker, "_send_message")

    email_service.send_inactive_account_was_deleted_email(user)

    assert mocked_email_func.call_count == 1

    call_data = mocked_email_func.call_args[0]
    assert call_data[0] == user.email
    assert call_data[1] == INACTIVE_ACCOUNT_DELETION_DONE_TEMPLATE


def test_send_reset_password_email(user, mocker):
    mocked_email_func = mock_email_service_function(mocker, "_send_message")

    email_service.send_reset_password_email(user)
    assert mocked_email_func.call_count == 1

    call_data = mocked_email_func.call_args[0]
    assert call_data[0] == user.email
    assert call_data[1] == USER_PASSWORD_RESET_EMAIL_TEMPLATE
    assert "RESET_PASSWORD_URL" in call_data[2]


def test_send_user_account_activation_email(user, mocker):
    mocked_email_func = mock_email_service_function(mocker, "_send_message")

    email_service.send_user_account_activation_email(user)
    assert mocked_email_func.call_count == 1

    call_data = mocked_email_func.call_args[0]
    assert call_data[0] == user.email
    assert call_data[1] == USER_ACCOUNT_VERIFICATION_EMAIL_TEMPLATE
    assert call_data[2] == {
        "SIGN_UP_VERIFICATION_URL": (
            f"{settings.PUBLIC_URL}/auth/sign-up/success/?hash={user.email}"
        )
    }
