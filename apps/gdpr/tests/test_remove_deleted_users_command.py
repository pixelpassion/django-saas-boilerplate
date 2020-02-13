from datetime import timedelta

from django.core.management import call_command
from django.utils import timezone

import pytest

from apps.users.models import User
from apps.users.tests.base_test_utils import mock_users_email_service_function

pytestmark = pytest.mark.django_db


def get_users_for_tests(user_factory):
    # create users with different last_login dates and is_deleted values
    for days in range(5, 10):
        last_login_date = timezone.now() - timedelta(days=days)
        user_factory(is_deleted=False, last_login=last_login_date)
        user_factory.create_batch(2, is_deleted=True, last_login=last_login_date)
    return User.objects.all()


def test_remove_deleted_users_command(user_factory, mocker):
    mocked_delete_email_func = mock_users_email_service_function(
        mocker, "send_account_was_deleted_email"
    )

    users = get_users_for_tests(user_factory)
    users_before_count = users.count()

    users_for_deletion_count = users.filter(
        last_login__lt=timezone.now() - timedelta(days=7), is_deleted=True
    ).count()

    call_command("remove_deleted_users")

    assert mocked_delete_email_func.call_count == users_for_deletion_count
    assert User.objects.count() == users_before_count - users_for_deletion_count


def test_remove_deleted_users_command_if_account_deletion_retention_in_days_is_zero(
    user_factory, mocker, settings
):
    settings.ACCOUNT_DELETION_RETENTION_IN_DAYS = 0
    mocked_delete_email_func = mock_users_email_service_function(
        mocker, "send_account_was_deleted_email"
    )

    users = get_users_for_tests(user_factory)
    users_before_count = users.count()

    call_command("remove_deleted_users")

    assert mocked_delete_email_func.call_count == 0
    assert User.objects.count() == users_before_count
