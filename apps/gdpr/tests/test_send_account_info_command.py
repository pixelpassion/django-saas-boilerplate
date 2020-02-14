import uuid
from datetime import timedelta

from django.core.management import call_command
from django.utils import timezone

import pytest

from apps.gdpr.management.commands.send_account_info import (
    Command as SendAccountInfoCommand,
)
from apps.users.tests.base_test_utils import mock_users_email_service_function

pytestmark = pytest.mark.django_db


def create_users_with_different_link_data(user_factory):
    # create users with different last_account_info_created
    # dates and account_info_link, account_info_sent values
    users_expired_link = user_factory.create_batch(
        2,
        account_info_link=uuid.uuid4(),
        last_account_info_created=timezone.now() - timedelta(days=10),
        account_info_sent=False,
    )
    users_expired_link_sent_data = user_factory.create_batch(
        3,
        account_info_link=uuid.uuid4(),
        last_account_info_created=timezone.now() - timedelta(days=10),
        account_info_sent=True,
    )
    users_valid_link = user_factory.create_batch(
        4,
        account_info_link=uuid.uuid4(),
        last_account_info_created=timezone.now(),
        account_info_sent=False,
    )
    user_factory.create_batch(
        5,
        account_info_link=uuid.uuid4(),
        last_account_info_created=timezone.now(),
        account_info_sent=True,
    )  # users with sent data

    return users_expired_link, users_expired_link_sent_data, users_valid_link


def test_send_account_info_command(user_factory, mocker):
    mocked_delete_email_func = mock_users_email_service_function(
        mocker, "send_account_info_is_ready_email"
    )
    (
        users_expired_link,
        users_expired_link_sent_data,
        users_valid_link,
    ) = create_users_with_different_link_data(user_factory)
    users_for_link_deletion = users_expired_link + users_expired_link_sent_data

    call_command("send_account_info")

    assert mocked_delete_email_func.call_count == len(users_valid_link)

    for user in users_for_link_deletion:
        user.refresh_from_db()
        assert user.account_info_link is None
        assert user.last_account_info_created is None
        assert not user.account_info_sent

    for user in users_valid_link:
        user.refresh_from_db()
        assert user.account_info_link is not None
        assert user.last_account_info_created is not None
        assert user.account_info_sent


def test_send_account_info_command_functions(user_factory):
    command = SendAccountInfoCommand()
    (
        users_expired_link,
        users_expired_link_sent_data,
        users_valid_link,
    ) = create_users_with_different_link_data(user_factory)

    users_for_link_deletion_count = len(users_expired_link) + len(
        users_expired_link_sent_data
    )
    assert (
        command._get_users_with_expired_link().count() == users_for_link_deletion_count
    )
    assert command._get_users_for_send_account_data_email().count() == len(
        users_valid_link
    )
