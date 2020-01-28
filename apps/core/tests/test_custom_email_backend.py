from django.core.mail import EmailMessage

import pytest

from apps.core.constants import (
    INVALID_ARG_TYPE_MESSAGE,
    INVALID_EMAIL_CLASS_USED_MESSAGE,
    SAASY_API_KEY_NOT_ASSIGNED_MESSAGE,
)
from apps.core.custom_email_backend import CustomEmailBackend, SaasyEmailMessage

DEFAULT_CONTEXT = {
    "first_context_variable": "Hello",
    "second_context_variable": "World",
}
RECIPIENT_EMAIL = "some@mail.com"
TEMPLATE_NAME = "some template"


def change_project_settings(settings):
    settings.SAASY_API_KEY = "some_key"
    settings.EMAIL_BACKEND = "apps.core.custom_email_backend.CustomEmailBackend"


def get_mocked_saasy_functions(mocker):
    mocked_create_mail_func = mocker.patch("saasy.client.Client.create_mail")
    mocked_create_mail_func.side_effect = lambda x: {"id": 1}
    mocked_send_mail_func = mocker.patch("saasy.client.Client.send_mail")

    return mocked_create_mail_func, mocked_send_mail_func


def test_custom_backend_send_email(settings, mocker):
    change_project_settings(settings)
    mocked_create_mail_func, mocked_send_mail_func = get_mocked_saasy_functions(mocker)

    email_message = SaasyEmailMessage(
        template=TEMPLATE_NAME, context=DEFAULT_CONTEXT, to=[RECIPIENT_EMAIL]
    )
    email_message.send()

    assert mocked_create_mail_func.call_count == 1
    assert mocked_send_mail_func.call_count == 1
    assert mocked_create_mail_func.call_args[0][0] == {
        "to_address": RECIPIENT_EMAIL,
        "context": DEFAULT_CONTEXT,
        "template": TEMPLATE_NAME,
    }
    assert mocked_send_mail_func.call_args[0][0] == 1


def test_custom_email_backend_correct_email_messages(settings, mocker):
    change_project_settings(settings)
    mocked_create_mail_func, mocked_send_mail_func = get_mocked_saasy_functions(mocker)

    email_message = SaasyEmailMessage(
        template=TEMPLATE_NAME, context=DEFAULT_CONTEXT, to=[RECIPIENT_EMAIL]
    )

    CustomEmailBackend().send_messages([email_message])

    assert mocked_create_mail_func.call_count == 1
    assert mocked_send_mail_func.call_count == 1
    assert mocked_create_mail_func.call_args[0][0] == {
        "to_address": RECIPIENT_EMAIL,
        "context": DEFAULT_CONTEXT,
        "template": TEMPLATE_NAME,
    }
    assert mocked_send_mail_func.call_args[0][0] == 1


def test_custom_email_backend_without_api_key(settings):
    settings.EMAIL_BACKEND = "apps.core.custom_email_backend.CustomEmailBackend"

    with pytest.raises(ValueError) as em:
        email_message = SaasyEmailMessage(
            template=TEMPLATE_NAME, context=DEFAULT_CONTEXT, to=[RECIPIENT_EMAIL]
        )
        email_message.send()
    assert SAASY_API_KEY_NOT_ASSIGNED_MESSAGE == em.value.args[0]


@pytest.mark.parametrize(
    "args",
    [
        {"context": DEFAULT_CONTEXT, "to": [RECIPIENT_EMAIL]},
        {"template": TEMPLATE_NAME, "to": [RECIPIENT_EMAIL]},
        {"to": [RECIPIENT_EMAIL]},
    ],
)
def test_custom_email_backend_email_message_without_needed_args(settings, mocker, args):
    change_project_settings(settings)
    mocked_create_mail_func, mocked_send_mail_func = get_mocked_saasy_functions(mocker)

    with pytest.raises(ValueError) as em:
        email_message = SaasyEmailMessage(**args)
        email_message.send()
    assert INVALID_EMAIL_CLASS_USED_MESSAGE == em.value.args[0]

    assert mocked_create_mail_func.call_count == 0
    assert mocked_send_mail_func.call_count == 0


def test_custom_email_backend_with_wrong_email_message_class(settings, mocker):
    change_project_settings(settings)
    mocked_create_mail_func, mocked_send_mail_func = get_mocked_saasy_functions(mocker)

    with pytest.raises(ValueError) as em:
        email_message = EmailMessage(to=[RECIPIENT_EMAIL])
        email_message.send()
    assert INVALID_EMAIL_CLASS_USED_MESSAGE == em.value.args[0]

    assert mocked_create_mail_func.call_count == 0
    assert mocked_send_mail_func.call_count == 0


def test_custom_email_backend_messages_without_recipients(settings, mocker):
    change_project_settings(settings)
    mocked_create_mail_func, mocked_send_mail_func = get_mocked_saasy_functions(mocker)

    email_message = SaasyEmailMessage(template=TEMPLATE_NAME, context=DEFAULT_CONTEXT)

    backend_response = CustomEmailBackend().send_messages([email_message])

    assert backend_response is False
    assert mocked_create_mail_func.call_count == 0
    assert mocked_send_mail_func.call_count == 0


def test_custom_email_backend_messages_without_messages(settings, mocker):
    change_project_settings(settings)
    mocked_create_mail_func, mocked_send_mail_func = get_mocked_saasy_functions(mocker)

    backend_response = CustomEmailBackend().send_messages([])

    assert backend_response is False
    assert mocked_create_mail_func.call_count == 0
    assert mocked_send_mail_func.call_count == 0


def test_create_saasy_email_message_invalid_arg_type():
    with pytest.raises(TypeError) as em:
        SaasyEmailMessage(context="some_context")
    assert em.value.args[0] == INVALID_ARG_TYPE_MESSAGE.format("context", "dict")


def test_create_saasy_email_message_invalid_template_arg_type():
    with pytest.raises(TypeError) as em:
        SaasyEmailMessage(template={"hello": "world"})
    assert em.value.args[0] == INVALID_ARG_TYPE_MESSAGE.format("template", "string")
