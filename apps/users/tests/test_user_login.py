from django.urls import reverse

import pytest
from trench.models import MFAMethod
from trench.utils import create_otp_code, create_secret

from .constants import GENERATE_CODE_URL, GENERATE_TOKEN_URL, TEST_EMAIL, TEST_PASSWORD

pytestmark = pytest.mark.django_db


def test_correct_login(user, client):
    payload = {"email": user.email, "password": TEST_PASSWORD}

    response = client.post(GENERATE_CODE_URL, payload)

    assert response.status_code == 200
    assert response.data["refresh"]
    assert response.data["access"]


def test_2fa_integration(user, logged_in_client, client):
    mfa_activate_url = reverse("v0:mfa-activate", args=["app"])
    # check that url present
    mfa_confirm = reverse("v0:mfa-activate-confirm", args=["app"])
    mfa_backup_codes = reverse("v0:mfa-regenerate-codes", args=["app"])
    mfa_deactivate = reverse("v0:mfa-deactivate", args=["app"])

    # Step 1: activate MFA
    response = logged_in_client.post(mfa_activate_url)
    assert response.status_code == 200
    qr_link = response.data.get("qr_link")
    assert qr_link
    assert MFAMethod.objects.filter(user=user).count() == 1
    secret = create_secret()
    # Step 2: confirm MFA (mocked step)
    assert not MFAMethod.objects.filter(
        user=user, is_active=True, is_primary=True
    ).exists()
    MFAMethod.objects.filter(user=user).update(secret=secret)
    response = logged_in_client.post(mfa_confirm, {"code": create_otp_code(secret)})
    assert response.status_code == 200
    assert response.data["backup_codes"]
    assert MFAMethod.objects.filter(user=user, is_active=True, is_primary=True).exists()

    # Step 3: trying to login
    payload = {"email": user.email, "password": TEST_PASSWORD}
    response = client.post(GENERATE_CODE_URL, payload)
    assert response.status_code == 200

    ephemeral_token = response.data["ephemeral_token"]
    payload = {"ephemeral_token": ephemeral_token, "code": create_otp_code(secret)}

    # Step 4: login with otp data
    response = client.post(GENERATE_TOKEN_URL, payload)
    assert response.status_code == 200
    assert response.data["access"]
    client.defaults["HTTP_AUTHORIZATION"] = f"Bearer {response.data['access']}"

    # Step 5: request backup codes
    response = client.post(mfa_backup_codes, {"code": create_otp_code(secret)})
    assert response.status_code == 200
    assert response.data["backup_codes"]

    # Step 6: deactivate
    code = response.data["backup_codes"][0]
    response = client.post(mfa_deactivate, {"code": code})
    assert response.status_code == 204
    assert MFAMethod.objects.filter(name="app").exists()
    assert not MFAMethod.objects.get(name="app").is_active


@pytest.mark.parametrize(
    "payload",
    [
        {"email": TEST_EMAIL, "password": "TEST_PASSWORD"},
        {"email": "asd@Asd.asd", "password": TEST_PASSWORD},
        {"email": "asd@Asd.asd", "password": "TEST_PASSWORD"},
    ],
)
def test_incorrect_login(user, client, payload):
    response = client.post(GENERATE_CODE_URL, payload)

    assert response.status_code != 200
    assert (
        response.data["messages"][0]
        == "No active account found with the given credentials"
    )


def test_correct_login_inactive_user(user, client):
    user.is_active = False
    user.save()
    payload = {"email": user.email, "password": TEST_PASSWORD}

    response = client.post(GENERATE_CODE_URL, payload)

    assert response.status_code == 401
    assert (
        response.data["messages"][0]
        == "No active account found with the given credentials"
    )


def test_login_username(user, client):
    response = client.post(
        GENERATE_CODE_URL, {"username": user.username, "password": TEST_PASSWORD}
    )

    assert response.status_code == 400
    assert response.data["messages"][0] == "email: This field is required."


def test_login_returned_data(client, user):
    payload = {"email": user.email, "password": TEST_PASSWORD}
    response = client.post(GENERATE_CODE_URL, payload)
    assert response.status_code == 200

    assert set(["refresh", "access"]) == set(
        [field for field, value in response.data.items()]
    )
