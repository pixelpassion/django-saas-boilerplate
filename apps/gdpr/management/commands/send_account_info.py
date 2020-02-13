from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.users.email_service import UsersSaasyEmailService
from apps.users.models import User


class Command(BaseCommand):
    help = "Sends a link to user data or deletes expired links"
    email_service = UsersSaasyEmailService()

    def __init__(self):
        super().__init__()
        self.settings_link_availability_days = (
            settings.ACCOUNT_INFO_LINK_AVAILABILITY_IN_DAYS
        )

    def _get_users_with_expired_link(self):
        return User.objects.filter(
            account_info_link__isnull=False,
            last_account_info_created__lt=timezone.now()
            - timedelta(days=self.settings_link_availability_days),
            account_info_sent__in=[True, False],
        )

    def _get_users_for_send_account_data_email(self):
        return User.objects.filter(
            account_info_link__isnull=False,
            last_account_info_created__gt=timezone.now()
            - timedelta(days=self.settings_link_availability_days),
            account_info_sent=False,
        )

    def run_send_account_info_command(self):
        users_with_expired_link = self._get_users_with_expired_link()
        users_for_send_account_data_email = (
            self._get_users_for_send_account_data_email()
        )

        for user in users_with_expired_link:
            user.delete_account_info_link()
        for user in users_for_send_account_data_email:
            self.email_service.send_account_info_is_ready_email(user)
            user.account_info_sent = True
            user.save(update_fields=["account_info_sent"])

    def handle(self, *args, **options):
        self.run_send_account_info_command()
