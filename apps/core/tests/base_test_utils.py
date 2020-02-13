from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def generate_uid_and_token(user):
    uuid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    return {"uuid": uuid, "token": token}


def get_mocked_saasy_functions(mocker):
    mocked_create_mail_func = mocker.patch("saasy.client.Client.create_mail")
    mocked_create_mail_func.side_effect = lambda x: {"id": 1}
    mocked_send_mail_func = mocker.patch("saasy.client.Client.send_mail")

    return mocked_create_mail_func, mocked_send_mail_func


def mock_email_backend_send_messages(mocker):
    return mocker.patch(
        f"apps.core.custom_email_backend.CustomEmailBackend.send_messages"
    )
