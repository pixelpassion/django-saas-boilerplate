import uuid
from datetime import timedelta

from django.core.management import call_command
from django.utils import timezone

import pytest

from apps.core.tests.base_test_utils import mock_email_service_function

pytestmark = pytest.mark.django_db


def test_send_account_info_command(user_factory, mocker):
    mocked_delete_email_func = mock_email_service_function(
        mocker, "send_account_info_is_ready_email"
    )
    # create users with different last_account_info_created
    # dates and account_info_link, account_info_sent values
    users_expired_link = user_factory.create_batch(
        5,
        account_info_link=uuid.uuid4(),
        last_account_info_created=timezone.now() - timedelta(days=10),
        account_info_sent=False,
    )
    users_expired_link_sent_data = user_factory.create_batch(
        5,
        account_info_link=uuid.uuid4(),
        last_account_info_created=timezone.now(),
        account_info_sent=True,
    )
    users_valid_link = user_factory.create_batch(
        5,
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

    users_for_link_deletion_count = len(users_expired_link) + len(
        users_expired_link_sent_data
    )

    call_command("send_account_info")

    assert mocked_delete_email_func.call_count == len(users_valid_link)

    for user in users_for_link_deletion_count:
        user.refresh_from_db()
        assert user.account_info_link is None
        assert user.last_account_info_created is None
        assert not user.account_info_sent

    for user in users_valid_link:
        user.refresh_from_db()
        assert user.account_info_link is not None
        assert user.last_account_info_created is not None
        assert user.account_info_sent
