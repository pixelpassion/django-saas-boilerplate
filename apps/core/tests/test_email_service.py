import pytest

from apps.core.email_service import BaseSaasyEmailService

pytestmark = pytest.mark.django_db

email_service = BaseSaasyEmailService()


def test_base_email_service_send_message(user, mocker):
    mail_id = 1
    mocked_create_mail_func = mocker.patch("saasy.client.Client.create_mail")
    mocked_create_mail_func.side_effect = lambda x: {"id": mail_id}
    mocked_send_mail_func = mocker.patch("saasy.client.Client.send_mail")

    template_name = "test_template"

    email = user.email
    context = {"first": 1, "second": 2}

    email_service._send_message(email, template_name, context)
    assert mocked_create_mail_func.call_count == 1
    assert mocked_send_mail_func.call_count == 1

    assert mocked_create_mail_func.call_args[0][0] == {
        "to_address": email,
        "context": context,
        "template": template_name,
    }
    assert mocked_send_mail_func.call_args[0][0] == mail_id
