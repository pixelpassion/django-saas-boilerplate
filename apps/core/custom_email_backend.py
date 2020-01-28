from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

from saasy.client import Client


class CustomEmailBackend(BaseEmailBackend):
    """
    Custom EmailBackend class for sending emails using the saasy package
    """

    def __init__(self, api_key=None, **kwargs):
        super().__init__()
        if not settings.SAASY_API_KEY:
            raise ValueError(
                "Set the SAASY_API_KEY in the project"
                " settings for using CustomEmailBackend"
            )
        self.saasy = Client(auth_token=settings.SAASY_API_KEY)

    def send_messages(self, email_messages):
        if not email_messages:
            return False

        for email_message in email_messages:
            recipients = email_message.recipients()
            if not recipients:
                return False

            for recipient in recipients:
                mail = self.saasy.create_mail(
                    {
                        "to_address": recipient,
                        "context": email_message.body,
                        "template": email_message.subject,
                    }
                )
                self.saasy.send_mail(mail["id"])
