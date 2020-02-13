from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.gdpr.email_service import GDPRSaasyEmailService
from apps.users.models import User


class Command(BaseCommand):
    help = "Deletes programmatically deleted users who logged in more than a week ago."
    email_service = GDPRSaasyEmailService()

    def run_remove_deleted_users_command(self):
        if settings.ACCOUNT_DELETION_RETENTION_IN_DAYS not in [0, None]:
            users = User.objects.filter(
                is_deleted=True, last_login__lt=timezone.now() - timedelta(days=7)
            )
            for user in users:
                self.email_service.send_account_was_deleted_email(user)
            users.delete()

    def handle(self, *args, **options):
        self.run_remove_deleted_users_command()
