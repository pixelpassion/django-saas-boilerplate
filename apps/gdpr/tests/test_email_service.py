from django.conf import settings as dj_settings

import pytest

from apps.gdpr.constants import (
    INACTIVE_ACCOUNT_DELETION_DONE_TEMPLATE,
    INACTIVE_ACCOUNT_DELETION_WARNING_TEMPLATE,
)
from apps.gdpr.email_service import GDPRSaasyEmailService

from .base_test_utils import mock_gdpr_email_service_function

pytestmark = pytest.mark.django_db

email_service = GDPRSaasyEmailService()


def test_send_inactive_account_was_deleted_email(user, mocker):
    mocked_email_func = mock_gdpr_email_service_function(mocker, "_send_message")
    bcc_email = dj_settings.INACTIVE_ACCOUNT_DELETION_BCC_EMAIL

    email_service.send_inactive_account_was_deleted_email(user)
    assert mocked_email_func.call_count == 2

    for index, sent_message in enumerate(mocked_email_func.call_args_list):
        call_data = sent_message[0]
        assert call_data[0] == user.email if index else bcc_email
        assert call_data[1] == INACTIVE_ACCOUNT_DELETION_DONE_TEMPLATE
        assert len(call_data) == 2


def test_send_inactive_account_was_deleted_email_if_deletion_bcc_email_is_none(
    user, mocker, settings
):
    settings.INACTIVE_ACCOUNT_DELETION_BCC_EMAIL = None
    mocked_email_func = mock_gdpr_email_service_function(mocker, "_send_message")

    email_service.send_inactive_account_was_deleted_email(user)
    assert mocked_email_func.call_count == 1

    call_data = mocked_email_func.call_args_list[0][0]
    assert call_data[0] == user.email
    assert call_data[1] == INACTIVE_ACCOUNT_DELETION_DONE_TEMPLATE
    assert len(call_data) == 2


def test_send_warning_about_upcoming_account_deletion(user, mocker):
    mocked_email_func = mock_gdpr_email_service_function(mocker, "_send_message")

    weeks = 5
    bcc_email = dj_settings.INACTIVE_ACCOUNT_WARNING_BCC_EMAIL
    email_service.send_warning_about_upcoming_account_deletion(user, weeks)

    assert mocked_email_func.call_count == 2

    for index, sent_message in enumerate(mocked_email_func.call_args_list):
        call_data = sent_message[0]
        assert call_data[0] == user.email if index else bcc_email
        assert call_data[1] == INACTIVE_ACCOUNT_DELETION_WARNING_TEMPLATE
        assert call_data[2] == {
            "WEEKS_LEFT": weeks,
            "PUBLIC_URL": dj_settings.PUBLIC_URL,
        }


def test_send_warning_about_upcoming_account_deletion_if_warning_bcc_email_is_none(
    user, mocker, settings
):
    settings.INACTIVE_ACCOUNT_WARNING_BCC_EMAIL = None
    mocked_email_func = mock_gdpr_email_service_function(mocker, "_send_message")

    weeks = 5
    email_service.send_warning_about_upcoming_account_deletion(user, weeks)

    assert mocked_email_func.call_count == 1

    call_data = mocked_email_func.call_args_list[0][0]
    assert call_data[0] == user.email
    assert call_data[1] == INACTIVE_ACCOUNT_DELETION_WARNING_TEMPLATE
    assert call_data[2] == {"WEEKS_LEFT": weeks, "PUBLIC_URL": dj_settings.PUBLIC_URL}
