from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from saasy.client import Client

from apps.core.custom_email_backend import SaasyEmailMessage

from .constants import (
    ACCOUNT_WAS_DELETED_EMAIL_TEMPLATE,
    ACCOUNT_WAS_RECOVERED_EMAIL_TEMPLATE,
    INACTIVE_ACCOUNT_DELETION_DONE_TEMPLATE,
    INACTIVE_ACCOUNT_DELETION_WARNING_TEMPLATE,
    USER_ACCOUNT_VERIFICATION_EMAIL_TEMPLATE,
    USER_PASSWORD_RESET_EMAIL_TEMPLATE,
)

saasy = Client(auth_token=settings.SAASY_API_KEY)


class SaasyEmailService:

    LOGIN_URL = f"{settings.PUBLIC_URL}/login"

    def _send_message(self, email, template_name, context={}):
        email_message = SaasyEmailMessage(
            template=template_name, context=context, to=[email]
        )
        email_message.send()

    def send_account_was_deleted_email(self, user: object):
        context = {"LOGIN_URL": self.LOGIN_URL}
        self._send_message(user.email, ACCOUNT_WAS_DELETED_EMAIL_TEMPLATE, context)

    def send_account_was_recovered_email(self, user: object):
        context = {"LOGIN_URL": self.LOGIN_URL}
        self._send_message(user.email, ACCOUNT_WAS_RECOVERED_EMAIL_TEMPLATE, context)

    def send_warning_about_upcoming_account_deletion(self, user: object, weeks: int):
        context = {"WEEKS_LEFT": weeks, "LOGIN_URL": self.LOGIN_URL}
        self._send_message(
            user.email, INACTIVE_ACCOUNT_DELETION_WARNING_TEMPLATE, context
        )

    def send_inactive_account_was_deleted_email(self, user: object):
        self._send_message(user.email, INACTIVE_ACCOUNT_DELETION_DONE_TEMPLATE)

    def send_reset_password_email(self, user: object):
        uuid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        context = {
            "RESET_PASSWORD_URL": (
                f"{settings.PUBLIC_URL}/auth/new-password?uid={uuid}&token={token}"
            )
        }
        self._send_message(user.email, USER_PASSWORD_RESET_EMAIL_TEMPLATE, context)

    def send_user_account_activation_email(self, user: object):
        # TODO: change context
        context = {
            "SIGN_UP_VERIFICATION_URL": (
                f"{settings.PUBLIC_URL}/auth/sign-up/success/?hash={user.email}"
            )
        }
        self._send_message(
            user.email, USER_ACCOUNT_VERIFICATION_EMAIL_TEMPLATE, context
        )
