from django.conf import settings

from apps.core.email_service import BaseSaasyEmailService

from .constants import (
    INACTIVE_ACCOUNT_DELETION_DONE_TEMPLATE,
    INACTIVE_ACCOUNT_DELETION_WARNING_TEMPLATE,
)


class GDPRSaasyEmailService(BaseSaasyEmailService):
    def send_inactive_account_was_deleted_email(self, user: object):
        settings_deletion_bcc_email = settings.INACTIVE_ACCOUNT_DELETION_BCC_EMAIL
        if settings_deletion_bcc_email:
            self._send_message(
                settings_deletion_bcc_email, INACTIVE_ACCOUNT_DELETION_DONE_TEMPLATE
            )
        self._send_message(user.email, INACTIVE_ACCOUNT_DELETION_DONE_TEMPLATE)

    def send_warning_about_upcoming_account_deletion(self, user: object, weeks: int):
        settings_warning_bcc_email = settings.INACTIVE_ACCOUNT_WARNING_BCC_EMAIL
        context = {"WEEKS_LEFT": weeks, "PUBLIC_URL": settings.PUBLIC_URL}
        if settings_warning_bcc_email:
            self._send_message(
                settings_warning_bcc_email,
                INACTIVE_ACCOUNT_DELETION_WARNING_TEMPLATE,
                context,
            )
        self._send_message(
            user.email, INACTIVE_ACCOUNT_DELETION_WARNING_TEMPLATE, context
        )
