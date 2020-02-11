from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.gdpr.email_service import SaasyEmailService
from apps.users.models import User


class Command(BaseCommand):
    help = "Deletes programmatically deleted users who logged in more than a week ago."
    email_service = SaasyEmailService()

    def handle(self, *args, **options):
        if settings.ACCOUNT_DELETION_RETENTION_IN_DAYS not in [0, None]:
            users = User.objects.filter(
                is_deleted=True, last_login__lt=timezone.now() - timedelta(days=7)
            )
            for user in users:
                self.email_service.send_account_was_deleted_email(user)
            users.delete()
