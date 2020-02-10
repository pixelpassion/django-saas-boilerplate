# from datetime import timedelta

# from django.conf import settings as project_settings
# from django.core.management import call_command
# from django.utils import timezone

# import pytest

# from apps.core.tests.base_tests_utils import mock_email_service_function
# from apps.gdpr.management.commands.delete_inactive_users import (
#     Command as DeleteInactiveUsersCommand,
# )
# from apps.users.models import User

# pytestmark = pytest.mark.django_db
# settings_weeks_deletion = (
#     project_settings.INACTIVE_ACCOUNT_DELETION_IN_WEEKS
# )  # default 52
# settings_weeks_warnings = (
#     project_settings.INACTIVE_ACCOUNT_WARNING_IN_WEEKS
# )  # default (1, 4)
# deletion_bcc_email = project_settings.INACTIVE_ACCOUNT_DELETION_BCC_EMAIL
# warning_bcc_email = project_settings.INACTIVE_ACCOUNT_WARNING_BCC_EMAIL


# def create_users_with_different_last_login_dates(user_factory):
#     for weeks in [2, 4, 5, 52, 55]:
#         if 1 < weeks < 4:
#             warning_sent_email = User.NO_WARNING
#         elif 4 <= weeks < 52:
#             warning_sent_email = User.WARNING_SENT_1_WEEK
#         else:
#             warning_sent_email = User.WARNING_SENT_4_WEEKS
#         user_factory(
#             is_deleted=True,
#             last_login=timezone.now() - timedelta(weeks=weeks),
#             warning_sent_email=warning_sent_email,
#         )


# def test_delete_inactive_users_command_if_settings_week_is_none(
#     user_factory, mocker, settings
# ):
#     settings.INACTIVE_ACCOUNT_DELETION_IN_WEEKS = None
#     create_users_with_different_last_login_dates(user_factory)

#     users_before = User.objects.count()

#     user_factory(
#         is_deleted=True,
#         last_login=timezone.now() - timedelta(weeks=4),
#         warning_sent_email=User.WARNING_SENT_4_WEEKS,
#     )

#     mocked_warning_emails_func = mock_email_service_function(
#         mocker, "send_warning_about_upcoming_account_deletion"
#     )
#     mocked_delete_email_func = mock_email_service_function(
#         mocker, "send_inactive_account_was_deleted_email"
#     )

#     call_command("delete_inactive_users")
#     assert mocked_warning_emails_func.call_count == 0
#     assert mocked_delete_email_func.call_count == 0
#     assert users_before == User.objects.count()


# def test_delete_inactive_users_command_flow(user_factory, mocker):
#     mocked_warning_emails_func = mock_email_service_function(
#         mocker, "send_warning_about_upcoming_account_deletion"
#     )
#     mocked_delete_email_func = mock_email_service_function(
#         mocker, "send_inactive_account_was_deleted_email"
#     )
#     create_users_with_different_last_login_dates(user_factory)

#     users_for_deletion_count = User.objects.filter(
#         last_login__lte=timezone.now() - timedelta(weeks=52),
#         warning_sent_email=User.WARNING_SENT_4_WEEKS,
#     ).count()
#     users_for_waring_count = User.objects.filter(
#         last_login__lt=timezone.now() - timedelta(weeks=1),
#         last_login__gt=timezone.now() - timedelta(weeks=52),
#     ).count()
#     users_before_count = User.objects.count()

#     call_command("delete_inactive_users")

#     assert mocked_warning_emails_func.call_count == users_for_waring_count
#     assert mocked_delete_email_func.call_count == users_for_deletion_count
#     assert User.objects.count() == users_before_count - users_for_deletion_count


# def test_delete_inactive_users_command_deletion_email_sending(user_factory, mocker):
#     user_factory(
#         is_deleted=True,
#         last_login=timezone.now() - timedelta(weeks=55),
#         warning_sent_email=User.WARNING_SENT_4_WEEKS,
#     )
#     mocked_email_func = mock_email_service_function(
#         mocker, "send_inactive_account_was_deleted_email"
#     )
#     call_command("delete_inactive_users")
#     assert mocked_email_func.call_count == 1


# @pytest.mark.parametrize(
#     "warning_sent_email_status", [User.WARNING_SENT_1_WEEK, User.NO_WARNING]
# )
# def test_delete_inactive_users_command_wrong_warning_sent_email_status(
#     user_factory, mocker, warning_sent_email_status
# ):
#     user_factory(
#         is_deleted=True,
#         last_login=timezone.now() - timedelta(weeks=55),
#         warning_sent_email=warning_sent_email_status,
#     )
#     mocked_email_func = mock_email_service_function(
#         mocker, "send_inactive_account_was_deleted_email"
#     )
#     call_command("delete_inactive_users")
#     assert mocked_email_func.call_count == 0


# @pytest.mark.parametrize("weeks", [2, 4, 5])
# def test_warning_inactive_users_command_warning_email_sending(
#     user_factory, mocker, weeks
# ):
#     user_factory(
#         is_deleted=True,
#         last_login=timezone.now() - timedelta(weeks=weeks),
#         warning_sent_email=User.WARNING_SENT_1_WEEK,
#     )
#     mocked_email_func = mock_email_service_function(
#         mocker, "send_warning_about_upcoming_account_deletion"
#     )
#     call_command("delete_inactive_users")
#     assert mocked_email_func.call_count == 1


# def test_warning_inactive_users_command_wrong_warning_sent_email_status(
#     user_factory, mocker
# ):
#     user_factory(
#         is_deleted=True,
#         last_login=timezone.now() - timedelta(weeks=4),
#         warning_sent_email=User.WARNING_SENT_4_WEEKS,
#     )
#     mocked_email_func = mock_email_service_function(
#         mocker, "send_warning_about_upcoming_account_deletion"
#     )
#     call_command("delete_inactive_users")
#     assert mocked_email_func.call_count == 0


# def test_delete_inactive_users_command_functions(user_factory):
#     command = DeleteInactiveUsersCommand()
#     create_users_with_different_last_login_dates(user_factory)

#     assert command._get_users_for_deletion().count() == 2
#     assert command._get_users_for_four_week_warning_email().count() == 2
#     assert command._get_users_for_one_week_warning_email().count() == 1


# @pytest.mark.parametrize("weeks", [1, 2, 3])
# def test_sent_email_inactive_users_one_week(user_factory, weeks, mocker):
#     mocked_email_func = mock_email_service_function(
#         mocker, "send_warning_about_upcoming_account_deletion"
#     )
#     user = user_factory(
#         is_deleted=True,
#         last_login=timezone.now() - timedelta(weeks=weeks),
#         warning_sent_email=User.NO_WARNING,
#     )

#     call_command("delete_inactive_users")
#     user.refresh_from_db()

#     assert mocked_email_func.call_count == 1
#     assert user.warning_sent_email == User.WARNING_SENT_1_WEEK


# @pytest.mark.parametrize("weeks", [4, 5, 50])
# def test_sent_email_inactive_users_four_week(user_factory, weeks, mocker):
#     mocked_email_func = mock_email_service_function(
#         mocker, "send_warning_about_upcoming_account_deletion"
#     )
#     user = user_factory(
#         is_deleted=True,
#         last_login=timezone.now() - timedelta(weeks=weeks),
#         warning_sent_email=User.WARNING_SENT_1_WEEK,
#     )

#     call_command("delete_inactive_users")
#     user.refresh_from_db()

#     assert mocked_email_func.call_count == 1
#     assert user.warning_sent_email == User.WARNING_SENT_4_WEEKS


# @pytest.mark.parametrize("weeks", [62, 53, 54])
# def test_sent_email_inactive_users_settings_week(user_factory, weeks, mocker):
#     mocked_email_func = mock_email_service_function(
#         mocker, "send_inactive_account_was_deleted_email"
#     )
#     user_factory(
#         is_deleted=True,
#         last_login=timezone.now() - timedelta(weeks=weeks),
#         warning_sent_email=User.WARNING_SENT_4_WEEKS,
#     )
#     users_before_count = User.objects.count()

#     call_command("delete_inactive_users")

#     assert mocked_email_func.call_count == 1
#     assert User.objects.count() == users_before_count - 1


# def test_delete_inactive_users_command_not_deleted_users(user_factory, mocker):
#     user_factory(
#         is_deleted=False,
#         last_login=timezone.now() - timedelta(weeks=55),
#         warning_sent_email=User.WARNING_SENT_4_WEEKS,
#     )
#     mocked_email_func = mock_email_service_function(
#         mocker, "send_inactive_account_was_deleted_email"
#     )
#     call_command("delete_inactive_users")
#     assert mocked_email_func.call_count == 0


# def test_warning_inactive_users_command_not_deleted_users(user_factory, mocker):
#     user_factory(
#         is_deleted=False,
#         last_login=timezone.now() - timedelta(weeks=5),
#         warning_sent_email=User.WARNING_SENT_1_WEEK,
#     )
#     mocked_email_func = mock_email_service_function(
#         mocker, "send_warning_about_upcoming_account_deletion"
#     )
#     call_command("delete_inactive_users")
#     assert mocked_email_func.call_count == 0
