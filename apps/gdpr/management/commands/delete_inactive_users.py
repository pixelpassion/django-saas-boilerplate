from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.gdpr.email_service import GDPRSaasyEmailService
from apps.users.models import User


class Command(BaseCommand):
    help = "Deletes inactive users and sends warning messages"
    email_service = GDPRSaasyEmailService()

    def __init__(self):
        super().__init__()
        self.settings_deletion_weeks = settings.INACTIVE_ACCOUNT_DELETION_IN_WEEKS
        self.settings_warning_weeks = settings.INACTIVE_ACCOUNT_WARNING_IN_WEEKS

    def _get_users_for_deletion(self):
        return User.objects.filter(
            is_deleted=False,
            warning_sent_email=User.SECOND_WARNING_SENT,
            last_login__lte=timezone.now()
            - timedelta(weeks=self.settings_deletion_weeks),
        )

    def _get_users_for_second_warning_email(self):
        return User.objects.filter(
            is_deleted=False,
            warning_sent_email=User.FIRST_WARNING_SENT,
            last_login__lt=timezone.now()
            - timedelta(weeks=self.settings_warning_weeks[0]),
            last_login__gt=timezone.now()
            - timedelta(weeks=self.settings_deletion_weeks),
        )

    def _get_users_for_first_warning_email(self):
        return User.objects.filter(
            is_deleted=False,
            warning_sent_email=User.NO_WARNING,
            last_login__lt=timezone.now()
            - timedelta(weeks=self.settings_warning_weeks[0]),
            last_login__gt=timezone.now()
            - timedelta(weeks=self.settings_warning_weeks[1]),
        )

    def run_delete_inactive_users_command(self):
        if self.settings_deletion_weeks:
            users_for_deletion = self._get_users_for_deletion()

            if self.settings_warning_weeks is not None:
                users_for_second_warning = self._get_users_for_second_warning_email()
                users_for_first_warning = self._get_users_for_first_warning_email()
                for users, weeks in {
                    users_for_second_warning: self.settings_warning_weeks[1],
                    users_for_first_warning: self.settings_warning_weeks[0],
                }.items():
                    for user in users:
                        self.email_service.send_warning_about_upcoming_account_deletion(
                            user, weeks
                        )
                    users.update(
                        warning_sent_email=User.FIRST_WARNING_SENT
                        if weeks == self.settings_warning_weeks[0]
                        else User.SECOND_WARNING_SENT
                    )
            for user in users_for_deletion:
                self.email_service.send_inactive_account_was_deleted_email(user)
            users_for_deletion.delete()

    def handle(self, *args, **options):
        self.run_delete_inactive_users_command()
