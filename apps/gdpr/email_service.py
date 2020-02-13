from django.conf import settings

from saasy.client import Client

from apps.core.email_service import BaseSaasyEmailService

from .constants import (
    ACCOUNT_WAS_DELETED_EMAIL_TEMPLATE,
    INACTIVE_ACCOUNT_DELETION_DONE_TEMPLATE,
    INACTIVE_ACCOUNT_DELETION_WARNING_TEMPLATE,
)

saasy = Client(auth_token=settings.SAASY_API_KEY)


class GDPRSaasyEmailService(BaseSaasyEmailService):
    def send_account_was_deleted_email(self, user: object):
        if user.is_deleted:
            settings_deleted_bcc_email = settings.ACCOUNT_DELETED_BCC_EMAIL
            if settings_deleted_bcc_email is not None:
                context = {"FROM_EMAIL": settings_deleted_bcc_email}
                self._send_message(
                    user.email, ACCOUNT_WAS_DELETED_EMAIL_TEMPLATE, context
                )
        else:
            settings_deletion_bcc_email = settings.INACTIVE_ACCOUNT_DELETION_BCC_EMAIL
            if settings_deletion_bcc_email is not None:
                context = {"FROM_EMAIL": settings_deletion_bcc_email}
                self._send_message(
                    user.email, INACTIVE_ACCOUNT_DELETION_DONE_TEMPLATE, context
                )

    def send_warning_about_upcoming_account_deletion(self, user: object, weeks: int):
        settings_warning_bcc_email = settings.INACTIVE_ACCOUNT_WARNING_BCC_EMAIL
        if settings_warning_bcc_email is not None:
            context = {
                "WEEKS_LEFT": weeks,
                "LOGIN_URL": self.LOGIN_URL,
                "FROM_EMAIL": settings_warning_bcc_email,
            }
            self._send_message(
                user.email, INACTIVE_ACCOUNT_DELETION_WARNING_TEMPLATE, context
            )
