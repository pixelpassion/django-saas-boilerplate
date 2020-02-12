import uuid
from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

import pytest

from apps.users.constants.messages import (
    USER_ALREADY_DELETED_MESSAGE,
    USER_WILL_BE_DELETED_MESSAGE,
)

pytestmark = pytest.mark.django_db


def test_soft_delete_user_invalid(user):
    user.is_deleted = True
    user.save()

    with pytest.raises(ValidationError) as em:
        user.soft_delete_user()
    assert USER_ALREADY_DELETED_MESSAGE in em.value

    # test user data
    user.refresh_from_db()
    assert user.is_deleted


def test_soft_delete_user_valid(user):
    user.is_deleted = False
    user.save()

    user.soft_delete_user()

    # test user data
    user.refresh_from_db()
    assert user.is_deleted


def test_soft_undelete_user_invalid(user):
    user.is_deleted = True
    user.last_login = timezone.now() - timedelta(
        days=settings.ACCOUNT_DELETION_RETENTION_IN_DAYS
    )
    user.save()

    with pytest.raises(ValidationError) as em:
        user.soft_undelete_user()
    assert USER_WILL_BE_DELETED_MESSAGE in em.value

    # test user data
    user.refresh_from_db()
    assert user.is_deleted


def test_soft_undelete_user_valid(user):
    user.is_deleted = True
    user.last_login = timezone.now() - timedelta(days=5)
    user.save()

    user.soft_undelete_user()

    # test user data
    user.refresh_from_db()
    assert not user.is_deleted


def test_create_account_info_link(user):
    assert user.account_info_link is None
    assert user.last_account_info_created is None
    assert not user.account_info_sent

    user.create_account_info_link()

    user.refresh_from_db()
    assert user.account_info_link is not None
    assert user.last_account_info_created is not None
    assert not user.account_info_sent


def test_recreate_account_info_link(user):
    user.account_info_link = uuid.uuid4()
    user.last_account_info_created = timezone.now()
    user.account_info_sent = True
    user.save()

    old_account_info_link = user.account_info_link
    old_last_account_info_created = user.last_account_info_created

    user.create_account_info_link()

    user.refresh_from_db()
    assert user.account_info_link != old_account_info_link
    assert user.last_account_info_created != old_last_account_info_created
    assert user.account_info_sent


def test_delete_account_info_link(user):
    user.account_info_link = uuid.uuid4()
    user.last_account_info_created = timezone.now()
    user.account_info_sent = True
    user.save()

    user.delete_account_info_link()

    assert user.account_info_link is None
    assert user.last_account_info_created is None
    assert not user.account_info_sent
