import uuid
from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

import pytest

from apps.gdpr.utils import account_info_handler
from apps.users.constants.messages import USER_ACCOUNT_INFO_HAS_ALREADY_BEEN_SENT
from apps.users.constants.url_names import GET_USER_DATA_URL_NAME

from .base_test_utils import mock_users_email_service_function
from .constants import CREATE_USER_DATA_LINK_URL

pytestmark = pytest.mark.django_db


def test_create_user_info_link_anon_user(client):
    response = client.post(CREATE_USER_DATA_LINK_URL)
    assert response.status_code == 401


def test_create_user_info_link_auth_user(logged_in_client, user, mocker):
    mocked_asked_for_email_func = mock_users_email_service_function(
        mocker, "send_account_info_asked_for_email"
    )
    mocked_account_info_is_ready_email_func = mock_users_email_service_function(
        mocker, "send_account_info_is_ready_email"
    )

    assert user.account_info_link is None
    assert user.last_account_info_created is None
    assert not user.account_info_sent

    response = logged_in_client.post(CREATE_USER_DATA_LINK_URL)
    assert response.status_code == 201

    user.refresh_from_db()
    assert user.account_info_link is not None
    assert user.last_account_info_created is not None
    assert user.account_info_sent

    assert mocked_asked_for_email_func.call_count == 1
    assert mocked_account_info_is_ready_email_func.call_count == 1


def test_create_user_info_user_data_already_sended(logged_in_client, user, mocker):
    mocked_asked_for_email_func = mock_users_email_service_function(
        mocker, "send_account_info_asked_for_email"
    )
    mocked_account_info_is_ready_email_func = mock_users_email_service_function(
        mocker, "send_account_info_is_ready_email"
    )

    user.account_info_link = uuid.uuid4()
    user.last_account_info_created = timezone.now()
    user.account_info_sent = True
    user.save()

    response = logged_in_client.post(CREATE_USER_DATA_LINK_URL)
    assert response.status_code == 400
    assert response.data == USER_ACCOUNT_INFO_HAS_ALREADY_BEEN_SENT

    user.refresh_from_db()
    assert user.account_info_link is not None
    assert user.last_account_info_created is not None
    assert user.account_info_sent

    assert mocked_asked_for_email_func.call_count == 0
    assert mocked_account_info_is_ready_email_func.call_count == 0


def test_create_user_info_link_auth_user_info_automated_is_false(
    logged_in_client, user, mocker, settings
):
    settings.ACCOUNT_INFO_AUTOMATED = False
    mocked_asked_for_email_func = mock_users_email_service_function(
        mocker, "send_account_info_asked_for_email"
    )
    mocked_account_info_is_ready_email_func = mock_users_email_service_function(
        mocker, "send_account_info_is_ready_email"
    )

    assert user.account_info_link is None
    assert user.last_account_info_created is None
    assert not user.account_info_sent

    response = logged_in_client.post(CREATE_USER_DATA_LINK_URL)
    assert response.status_code == 201

    user.refresh_from_db()
    assert user.account_info_link is None
    assert user.last_account_info_created is None
    assert not user.account_info_sent

    assert mocked_asked_for_email_func.call_count == 1
    assert mocked_account_info_is_ready_email_func.call_count == 0


def test_get_user_info_link_anon_user(client):
    response = client.post(CREATE_USER_DATA_LINK_URL, args=["some_hash"])
    assert response.status_code == 401


def test_get_user_info_link_auth_user(logged_in_client, user):
    user.account_info_link = uuid.uuid4()
    user.last_account_info_created = timezone.now()
    user.save()

    user.refresh_from_db()

    response = logged_in_client.get(
        reverse(f"v0:{GET_USER_DATA_URL_NAME}", args=[str(user.account_info_link)])
    )
    assert response.status_code == 200
    assert response.data == account_info_handler(user)


def test_get_user_info_link_auth_user_expired_link(logged_in_client, user):
    user.account_info_link = uuid.uuid4()
    user.last_account_info_created = timezone.now() - timedelta(days=8)
    user.save()

    user.refresh_from_db()

    response = logged_in_client.get(
        reverse(f"v0:{GET_USER_DATA_URL_NAME}", args=[str(user.account_info_link)])
    )
    assert response.status_code == 404


def test_get_user_info_link_auth_user_fake_link(logged_in_client, user, settings):
    user.account_info_link = uuid.uuid4()
    user.last_account_info_created = timezone.now()
    user.save()

    user.refresh_from_db()

    response = logged_in_client.get(
        reverse(f"v0:{GET_USER_DATA_URL_NAME}", args=[uuid.uuid4()])
    )
    assert response.status_code == 404


def test_get_user_info_link_other_user(logged_in_client, user_factory):
    other_user = user_factory(
        account_info_link=uuid.uuid4(), last_account_info_created=timezone.now()
    )

    response = logged_in_client.get(
        reverse(
            f"v0:{GET_USER_DATA_URL_NAME}", args=[str(other_user.account_info_link)]
        )
    )
    assert response.status_code == 404
