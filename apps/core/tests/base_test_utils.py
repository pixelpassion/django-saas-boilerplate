from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def set_custom_email_backend_settings(settings):
    settings.SAASY_API_KEY = "some_key"
    settings.EMAIL_BACKEND = "apps.core.custom_email_backend.CustomEmailBackend"


def generate_uid_and_token(user):
    uuid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    return {"uuid": uuid, "token": token}


def mock_email_backend_send_messages(mocker, settings):
    settings.SAASY_API_KEY = "some_key"
    settings.EMAIL_BACKEND = "apps.core.custom_email_backend.CustomEmailBackend"
    return mocker.patch(
        f"apps.core.custom_email_backend.CustomEmailBackend.send_messages"
    )


def mock_email_service_function(mocker, func_name):
    return mocker.patch(f"apps.gdpr.email_service.SaasyEmailService.{func_name}")
