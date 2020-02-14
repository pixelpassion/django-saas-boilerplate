import pytest

from apps.gdpr.utils import account_info_handler

pytestmark = pytest.mark.django_db


def test_account_info_handler(user):
    needed_data = {
        "email": user.email,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "privacy_policy": user.privacy_policy,
        "warning_sent_email": user.warning_sent_email,
        "account_info_link": user.account_info_link,
        "last_account_info_created": None,
        "is_staff": user.is_staff,
        "is_active": user.is_active,
        "date_joined": user.date_joined.strftime("%d/%m/%Y %H:%m:%S"),
        "last_login": None,
        "last_password_change_date": user.last_password_change_date.strftime(
            "%d/%m/%Y %H:%m:%S"
        ),
    }
    assert account_info_handler(user) == needed_data
