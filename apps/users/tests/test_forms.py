import pytest

from apps.core.tests.base_test_utils import mock_email_backend_send_messages
from apps.users.forms import CustomPasswordResetForm

pytestmark = pytest.mark.django_db


def test_password_reset_form_with_valid_email(user, mocker, settings):
    mocked_email_func = mock_email_backend_send_messages(mocker, settings)
    form_data = {"email": user.email}
    form = CustomPasswordResetForm(data=form_data)

    assert form.is_valid()
    form.save()
    assert mocked_email_func.call_count == 1


def test_password_reset_form_with_invalid_email(user, mocker, settings):
    mocked_email_func = mock_email_backend_send_messages(mocker, settings)
    form_data = {"email": "invalid@mail.com"}
    form = CustomPasswordResetForm(data=form_data)

    assert form.is_valid()
    form.save()
    assert mocked_email_func.call_count == 0


def test_password_reset_form_without_email():
    form_data = {"email": ""}
    form = CustomPasswordResetForm(data=form_data)

    assert not form.is_valid()
    assert form.errors["email"][0] == "This field is required."
