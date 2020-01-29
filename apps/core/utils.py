from django.conf import settings
from django.core.mail import EmailMessage

from apps.core.custom_email_backend import SaasyEmailMessage

from .constants import NO_RELEVANT_VALUES_IN_THE_CONTEXT_MESSAGE


def create_and_send_email(template_name, context, to_address):
    if settings.SAASY_API_KEY:
        email_message = SaasyEmailMessage(
            template=template_name, context=context, to=[to_address]
        )
    else:
        ver_url = context.get("verification_url")
        if not ver_url:
            raise ValueError(NO_RELEVANT_VALUES_IN_THE_CONTEXT_MESSAGE)
        if template_name == "email-activation":
            body = f"Hello! Here is your sign up verification link: {ver_url}"
        elif template_name == "password-forget":
            body = (
                f"Hello! Please click here to verify and setup a new password {ver_url}"
            )
        email_message = EmailMessage(
            context["subject"], body, settings.DEFAULT_FROM_EMAIL, [to_address]
        )
    email_message.send()
