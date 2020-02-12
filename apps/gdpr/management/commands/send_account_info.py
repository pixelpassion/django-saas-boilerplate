from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.gdpr.email_service import SaasyEmailService
from apps.users.models import User


class Command(BaseCommand):
    help = "Deletes inactive users and sends warning messages"
    email_service = SaasyEmailService()

    def __init__(self):
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

    def handle(self, *args, **options):
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
