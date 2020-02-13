from django.conf import settings as dj_settings

import pytest

from apps.users.constants.template_names import (
    ACCOUNT_INFO_ASKED_FOR_TEMPLATE,
    ACCOUNT_INFO_IS_READY_TEMPLATE,
    ACCOUNT_SCHEDULED_FOR_DELETION_TEMPLATE_NAME,
    ACCOUNT_WAS_DELETED_EMAIL_TEMPLATE,
    ACCOUNT_WAS_RECOVERED_EMAIL_TEMPLATE,
    USER_ACCOUNT_VERIFICATION_EMAIL_TEMPLATE,
    USER_PASSWORD_RESET_EMAIL_TEMPLATE,
)
from apps.users.email_service import UsersSaasyEmailService

from .base_test_utils import mock_users_email_service_function

pytestmark = pytest.mark.django_db

email_service = UsersSaasyEmailService()


def test_send_account_was_deleted_email(user, mocker):
    mocked_email_func = mock_users_email_service_function(mocker, "_send_message")
    bcc_email = dj_settings.ACCOUNT_DELETED_BCC_EMAIL

    user.is_deleted = True
    user.save()

    email_service.send_account_was_deleted_email(user)
    assert mocked_email_func.call_count == 2

    for index, sent_message in enumerate(mocked_email_func.call_args_list):
        call_data = sent_message[0]
        assert call_data[0] == user.email if index else bcc_email
        assert call_data[1] == ACCOUNT_WAS_DELETED_EMAIL_TEMPLATE
        assert len(call_data) == 2


def test_send_account_was_deleted_email_if_deleted_bcc_email_is_none(
    user, mocker, settings
):
    settings.ACCOUNT_DELETED_BCC_EMAIL = None
    mocked_email_func = mock_users_email_service_function(mocker, "_send_message")

    user.is_deleted = True
    user.save()

    email_service.send_account_was_deleted_email(user)
    assert mocked_email_func.call_count == 1

    call_data = mocked_email_func.call_args_list[0][0]
    assert call_data[0] == user.email
    assert call_data[1] == ACCOUNT_WAS_DELETED_EMAIL_TEMPLATE
    assert len(call_data) == 2


def test_send_account_was_recovered_email(user, mocker):
    mocked_email_func = mock_users_email_service_function(mocker, "_send_message")

    email_service.send_account_was_recovered_email(user)
    assert mocked_email_func.call_count == 1

    call_data = mocked_email_func.call_args[0]
    assert call_data[0] == user.email
    assert call_data[1] == ACCOUNT_WAS_RECOVERED_EMAIL_TEMPLATE
    assert len(call_data) == 2


def test_send_reset_password_email(user, mocker):
    mocked_email_func = mock_users_email_service_function(mocker, "_send_message")

    email_service.send_reset_password_email(user)
    assert mocked_email_func.call_count == 1

    call_data = mocked_email_func.call_args[0]
    assert call_data[0] == user.email
    assert call_data[1] == USER_PASSWORD_RESET_EMAIL_TEMPLATE
    assert "PUBLIC_URL" in call_data[2]
    assert "UUID" in call_data[2]
    assert "TOKEN" in call_data[2]


def test_send_user_account_activation_email(user, mocker):
    mocked_email_func = mock_users_email_service_function(mocker, "_send_message")

    email_service.send_user_account_activation_email(user)
    assert mocked_email_func.call_count == 1

    call_data = mocked_email_func.call_args[0]
    assert call_data[0] == user.email
    assert call_data[1] == USER_ACCOUNT_VERIFICATION_EMAIL_TEMPLATE
    assert call_data[2] == {"PUBLIC_URL": dj_settings.PUBLIC_URL}


def test_send_account_scheduled_for_deletion_email(user, mocker):
    mocked_email_func = mock_users_email_service_function(mocker, "_send_message")
    bcc_email = dj_settings.ACCOUNT_SCHEDULED_FOR_DELETION_BCC_EMAIL

    email_service.send_account_scheduled_for_deletion_email(user)
    assert mocked_email_func.call_count == 2

    for index, sent_message in enumerate(mocked_email_func.call_args_list):
        call_data = sent_message[0]
        assert call_data[0] == user.email if index else bcc_email
        assert call_data[1] == ACCOUNT_SCHEDULED_FOR_DELETION_TEMPLATE_NAME
        assert len(call_data) == 2


def test_send_account_scheduled_for_deletion_email_if_scheduled_bcc_email_is_none(
    user, mocker, settings
):
    settings.ACCOUNT_SCHEDULED_FOR_DELETION_BCC_EMAIL = None
    mocked_email_func = mock_users_email_service_function(mocker, "_send_message")

    email_service.send_account_scheduled_for_deletion_email(user)
    assert mocked_email_func.call_count == 1

    call_data = mocked_email_func.call_args_list[0][0]
    assert call_data[0] == user.email
    assert call_data[1] == ACCOUNT_SCHEDULED_FOR_DELETION_TEMPLATE_NAME
    assert len(call_data) == 2


@pytest.mark.parametrize("in_days_value", [0, None])
def test_send_account_scheduled_for_deletion_email_if_deletion_retention(
    user, mocker, settings, in_days_value
):
    settings.ACCOUNT_DELETION_RETENTION_IN_DAYS = in_days_value
    mocked_email_func = mock_users_email_service_function(mocker, "_send_message")

    email_service.send_account_scheduled_for_deletion_email(user)
    assert mocked_email_func.call_count == 0


def test_send_account_info_asked_for_email(user, mocker):
    mocked_email_func = mock_users_email_service_function(mocker, "_send_message")
    bcc_email = dj_settings.ACCOUNT_INFO_ASKED_FOR_EMAIL

    email_service.send_account_info_asked_for_email(user)
    assert mocked_email_func.call_count == 2

    for index, sent_message in enumerate(mocked_email_func.call_args_list):
        call_data = sent_message[0]
        assert call_data[0] == user.email if index else bcc_email
        assert call_data[1] == ACCOUNT_INFO_ASKED_FOR_TEMPLATE
        assert len(call_data) == 2


def test_send_account_info_is_ready_email(user, mocker):
    mocked_email_func = mock_users_email_service_function(mocker, "_send_message")
    user.create_account_info_link()

    email_service.send_account_info_is_ready_email(user)
    assert mocked_email_func.call_count == 1

    call_data = mocked_email_func.call_args[0]
    assert call_data[0] == user.email
    assert call_data[1] == ACCOUNT_INFO_IS_READY_TEMPLATE
    assert call_data[2] == {
        "PUBLIC_URL": dj_settings.PUBLIC_URL,
        "ACCOUNT_INFO_LINK": str(user.account_info_link),
        "ACCOUNT_INFO_LINK_AVAILABILITY_IN_DAYS": (
            dj_settings.ACCOUNT_INFO_LINK_AVAILABILITY_IN_DAYS
        ),
        "GDPR_SUPPORT_EMAIL": dj_settings.GDPR_SUPPORT_EMAIL,
    }


def test_send_account_info_asked_for_email_if_settings_email_is_none(
    user, mocker, settings
):
    settings.ACCOUNT_INFO_ASKED_FOR_EMAIL = None
    mocked_email_func = mock_users_email_service_function(mocker, "_send_message")

    email_service.send_account_info_asked_for_email(user)
    assert mocked_email_func.call_count == 1

    call_data = mocked_email_func.call_args_list[0][0]
    assert call_data[0] == user.email
    assert call_data[1] == ACCOUNT_INFO_ASKED_FOR_TEMPLATE
    assert len(call_data) == 2
