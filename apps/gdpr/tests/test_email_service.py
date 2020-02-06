from django.conf import settings as project_settings

import pytest

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


def mock_email_service_function(mocker, settings, func_name):
    settings.SAASY_API_KEY = "some_key"
    settings.EMAIL_BACKEND = "apps.core.custom_email_backend.CustomEmailBackend"
    return mocker.patch(f"apps.gdpr.email_service.SaasyEmailService.{func_name}")


def test_send_account_was_deleted_email(user, mocker, settings):
    mocked_email_func = mock_email_service_function(mocker, settings, "_send_message")

    email_service.send_account_was_deleted_email(user)
    assert mocked_email_func.call_count == 1

    call_data = mocked_email_func.call_args[0]
    assert call_data[0] == user.email
    assert call_data[1] == ACCOUNT_WAS_DELETED_EMAIL_TEMPLATE


def test_send_account_was_recovered_email(user, mocker, settings):
    mocked_email_func = mock_email_service_function(mocker, settings, "_send_message")

    email_service.send_account_was_recovered_email(user)
    assert mocked_email_func.call_count == 1

    call_data = mocked_email_func.call_args[0]
    assert call_data[0] == user.email
    assert call_data[1] == ACCOUNT_WAS_RECOVERED_EMAIL_TEMPLATE


def test_send_warning_about_upcoming_account_deletion(user, mocker, settings):
    mocked_email_func = mock_email_service_function(mocker, settings, "_send_message")

    weeks = 5
    email_service.send_warning_about_upcoming_account_deletion(user, weeks)

    assert mocked_email_func.call_count == 1

    call_data = mocked_email_func.call_args[0]
    assert call_data[0] == user.email
    assert call_data[1] == INACTIVE_ACCOUNT_DELETION_WARNING_TEMPLATE
    assert call_data[2] == {
        "WEEKS_LEFT": weeks,
        "LOGIN_URL": f"{project_settings.PUBLIC_URL}/login",
    }


def test_send_inactive_account_was_deleted_email(user, mocker, settings):
    mocked_email_func = mock_email_service_function(mocker, settings, "_send_message")

    email_service.send_inactive_account_was_deleted_email(user)

    assert mocked_email_func.call_count == 1

    call_data = mocked_email_func.call_args[0]
    assert call_data[0] == user.email
    assert call_data[1] == INACTIVE_ACCOUNT_DELETION_DONE_TEMPLATE


def test_send_reset_password_email(user, mocker, settings):
    mocked_email_func = mock_email_service_function(mocker, settings, "_send_message")

    email_service.send_reset_password_email(user)
    assert mocked_email_func.call_count == 1

    call_data = mocked_email_func.call_args[0]
    assert call_data[0] == user.email
    assert call_data[1] == USER_PASSWORD_RESET_EMAIL_TEMPLATE
    assert "RESET_PASSWORD_URL" in call_data[2]


def test_send_user_account_activation_email(user, mocker, settings):
    mocked_email_func = mock_email_service_function(mocker, settings, "_send_message")

    email_service.send_user_account_activation_email(user)
    assert mocked_email_func.call_count == 1

    call_data = mocked_email_func.call_args[0]
    assert call_data[0] == user.email
    assert call_data[1] == USER_ACCOUNT_VERIFICATION_EMAIL_TEMPLATE
    assert call_data[2] == {
        "SIGN_UP_VERIFICATION_URL": (
            f"{project_settings.PUBLIC_URL}/auth/sign-up/success/?hash={user.email}"
        )
    }
