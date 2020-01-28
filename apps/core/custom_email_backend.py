from django.core.mail.backends.base import BaseEmailBackend

# from django.core.mail.backends.smtp import EmailBackend


class CustomEmailBackend(BaseEmailBackend):
    """
    Custom EmailBackend class for sending emails using the saasy package
    """

    def send_messages(self, email_messages):
        pass
