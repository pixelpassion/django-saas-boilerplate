import sys
from importlib import reload

from django.urls import clear_url_caches

import pytest

pytestmark = pytest.mark.django_db
DOCS_URL = "/docs/"


@pytest.fixture
def all_urlconfs():
    return [
        "apps.core.urls",
        "apps.users.urls",
        "conf.urls",  # The ROOT_URLCONF must be last!
    ]


@pytest.fixture
def reloaded_urlconfs(all_urlconfs):
    def _reloaded_urlconfs():
        """
        Use this to ensure all urlconfs are reloaded as needed before the test.
        """

        clear_url_caches()
        for urlconf in all_urlconfs:
            if urlconf in sys.modules:
                reload(sys.modules[urlconf])

    return _reloaded_urlconfs


def test_docs_view_public_api_doc_true(client, settings, reloaded_urlconfs):
    """Test docs view when PUBLIC_API_DOCUMENTATION is True."""
    settings.STATICFILES_STORAGE = (
        "django.contrib.staticfiles.storage.StaticFilesStorage"
    )
    # added because swagger need statifiles to show web page
    settings.PUBLIC_API_DOCUMENTATION = True
    settings.DEBUG = False
    reloaded_urlconfs()
    response = client.get(DOCS_URL)
    assert response.status_code == 200


def test_docs_view_debug_true(client, settings, reloaded_urlconfs):
    """Test docs view when DEBUG is True."""
    settings.STATICFILES_STORAGE = (
        "django.contrib.staticfiles.storage.StaticFilesStorage"
    )
    # added because swagger need statifiles to show web page
    settings.DEBUG = True
    settings.PUBLIC_API_DOCUMENTATION = False
    reloaded_urlconfs()
    response = client.get(DOCS_URL)
    assert response.status_code == 200


def test_docs_view_env_false(client, settings, reloaded_urlconfs):
    """Test docs view when PUBLIC_API_DOCUMENTATION is False."""
    settings.PUBLIC_API_DOCUMENTATION = False
    settings.DEBUG = False
    reloaded_urlconfs()
    response = client.get(DOCS_URL)
    assert response.status_code == 404
