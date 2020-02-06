""" This file contains global level fixtures for the pytest
"""
import os
import shutil

from django.conf import settings

import pytest
from pytest_factoryboy import register

from apps.users.tests.constants import TEST_EMAIL, TEST_PASSWORD, TOKEN_OBTAIN_PAIR_URL
from apps.users.tests.factories import UserFactory


@pytest.fixture()
def logged_in_client(user, client):
    response = client.post(
        TOKEN_OBTAIN_PAIR_URL, {"email": user.email, "password": TEST_PASSWORD}
    )
    assert response.status_code == 200
    client.defaults["HTTP_AUTHORIZATION"] = f"Bearer {response.data['access']}"
    return client


@pytest.fixture(scope="session", autouse=True)
def remove_tempdir(request):
    """ This fixture remove temporary directory created for the media root
    """

    def fin():
        if all([os.path.isdir(settings.MEDIA_ROOT), "test" == settings.ENV]):
            shutil.rmtree(settings.MEDIA_ROOT)

    request.addfinalizer(fin)


register(UserFactory, email=TEST_EMAIL)
