from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apps.core.email_service import BaseSaasyEmailService

from .constants.template_names import (
    ACCOUNT_INFO_ASKED_FOR_TEMPLATE,
    ACCOUNT_INFO_IS_READY_TEMPLATE,
    ACCOUNT_SCHEDULED_FOR_DELETION_TEMPLATE_NAME,
    ACCOUNT_WAS_DELETED_EMAIL_TEMPLATE,
    ACCOUNT_WAS_RECOVERED_EMAIL_TEMPLATE,
    USER_ACCOUNT_VERIFICATION_EMAIL_TEMPLATE,
    USER_PASSWORD_RESET_EMAIL_TEMPLATE,
)


class UsersSaasyEmailService(BaseSaasyEmailService):
    def send_account_was_deleted_email(self, user: object):
        settings_deleted_bcc_email = settings.ACCOUNT_DELETED_BCC_EMAIL
        if settings_deleted_bcc_email:
            self._send_message(
                settings_deleted_bcc_email, ACCOUNT_WAS_DELETED_EMAIL_TEMPLATE
            )
        self._send_message(user.email, ACCOUNT_WAS_DELETED_EMAIL_TEMPLATE)

    def send_account_was_recovered_email(self, user: object):
        self._send_message(user.email, ACCOUNT_WAS_RECOVERED_EMAIL_TEMPLATE)

    def send_reset_password_email(self, user: object):
        uuid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        context = {"PUBLIC_URL": settings.PUBLIC_URL, "UUID": uuid, "TOKEN": token}
        self._send_message(user.email, USER_PASSWORD_RESET_EMAIL_TEMPLATE, context)

    def send_user_account_activation_email(self, user: object):
        # TODO: change context
        context = {"PUBLIC_URL": settings.PUBLIC_URL}
        self._send_message(
            user.email, USER_ACCOUNT_VERIFICATION_EMAIL_TEMPLATE, context
        )

    def send_account_scheduled_for_deletion_email(self, user: object):
        settings_account_scheduled_bcc_email = (
            settings.ACCOUNT_SCHEDULED_FOR_DELETION_BCC_EMAIL
        )
        settings_account_deletion_in_days = settings.ACCOUNT_DELETION_RETENTION_IN_DAYS
        if settings_account_deletion_in_days:
            if settings_account_scheduled_bcc_email:
                self._send_message(
                    settings_account_scheduled_bcc_email,
                    ACCOUNT_SCHEDULED_FOR_DELETION_TEMPLATE_NAME,
                )
            self._send_message(user.email, ACCOUNT_SCHEDULED_FOR_DELETION_TEMPLATE_NAME)

    def send_account_info_asked_for_email(self, user: object):
        settings_account_info_asked_for_email = settings.ACCOUNT_INFO_ASKED_FOR_EMAIL
        if settings_account_info_asked_for_email:
            self._send_message(
                settings_account_info_asked_for_email, ACCOUNT_INFO_ASKED_FOR_TEMPLATE
            )
        self._send_message(user.email, ACCOUNT_INFO_ASKED_FOR_TEMPLATE)

    def send_account_info_is_ready_email(self, user: object):
        context = {
            "PUBLIC_URL": settings.PUBLIC_URL,
            "ACCOUNT_INFO_LINK": str(user.account_info_link),
            "ACCOUNT_INFO_LINK_AVAILABILITY_IN_DAYS": (
                settings.ACCOUNT_INFO_LINK_AVAILABILITY_IN_DAYS
            ),
            "GDPR_SUPPORT_EMAIL": settings.GDPR_SUPPORT_EMAIL,
        }
        self._send_message(user.email, ACCOUNT_INFO_IS_READY_TEMPLATE, context)
