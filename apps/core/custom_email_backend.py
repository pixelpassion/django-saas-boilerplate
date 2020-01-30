from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail.backends.base import BaseEmailBackend

from saasy.client import Client

from .constants import (
    INVALID_ARG_TYPE_MESSAGE,
    INVALID_EMAIL_CLASS_USED_MESSAGE,
    SAASY_API_KEY_NOT_ASSIGNED_MESSAGE,
)


class SaasyEmailMessage(EmailMessage):
    """ Added two new arguments (context, template) for working with saasy
    """

    def __init__(
        self,
        context: dict,
        template: str,
        subject="",
        body="",
        from_email=None,
        to=None,
        bcc=None,
        connection=None,
        attachments=None,
        headers=None,
        cc=None,
        reply_to=None,
    ):
        super().__init__(
            subject,
            body,
            from_email,
            to,
            bcc,
            connection,
            attachments,
            headers,
            cc,
            reply_to,
        )
        if not isinstance(context, dict):
            raise TypeError(INVALID_ARG_TYPE_MESSAGE.format("context", "dict"))
        self.context = context
        if not isinstance(template, str):
            raise TypeError(INVALID_ARG_TYPE_MESSAGE.format("template", "string"))
        self.template = template


class CustomEmailBackend(BaseEmailBackend):
    """
    Custom EmailBackend class for sending emails using the saasy package
    """

    def __init__(self, api_key=None, **kwargs):
        super().__init__()
        if not settings.SAASY_API_KEY:
            raise ValueError(SAASY_API_KEY_NOT_ASSIGNED_MESSAGE)
        self.saasy = Client(auth_token=settings.SAASY_API_KEY)

    def send_messages(self, email_messages):
        if not email_messages:
            return None

        for email_message in email_messages:
            if not isinstance(email_message, SaasyEmailMessage):
                raise ValueError(INVALID_EMAIL_CLASS_USED_MESSAGE)
            context = email_message.context
            template = email_message.template
            recipients = email_message.recipients()
            if not recipients:
                continue

            for recipient in recipients:
                mail = self.saasy.create_mail(
                    {"to_address": recipient, "context": context, "template": template}
                )
                self.saasy.send_mail(mail["id"])
