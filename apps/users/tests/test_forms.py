import pytest

from apps.core.tests.base_test_utils import mock_email_backend_send_messages
from apps.users.forms import CustomPasswordResetForm, CustomSetPasswordForm

from .constants import NEW_TEST_PASSWORD

pytestmark = pytest.mark.django_db


def test_password_reset_form_with_valid_email(user, mocker):
    mocked_email_func = mock_email_backend_send_messages(mocker)
    form_data = {"email": user.email}
    form = CustomPasswordResetForm(data=form_data)

    assert form.is_valid()
    form.save()
    assert mocked_email_func.call_count == 1


def test_password_reset_form_with_invalid_email(user, mocker):
    mocked_email_func = mock_email_backend_send_messages(mocker)
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


def test_password_set_form_with_last_password_change_date(user):
    user_old_last_password_change_date = user.last_password_change_date
    form_data = {"new_password1": NEW_TEST_PASSWORD, "new_password2": NEW_TEST_PASSWORD}
    assert not user.check_password(NEW_TEST_PASSWORD)
    form = CustomSetPasswordForm(data=form_data, user=user)

    assert form.is_valid()
    form.save()
    user.refresh_from_db()
    assert user_old_last_password_change_date != user.last_password_change_date
    assert user.check_password(NEW_TEST_PASSWORD)
