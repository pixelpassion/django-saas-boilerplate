""" This file contains global level fixtures for the pytest
"""
import os
import shutil

from django.conf import settings

import pytest


@pytest.fixture(scope="session", autouse=True)
def remove_tempdir(request):
    """ This fixture remove temporary directory created for the media root
    """

    def fin():
        if all([os.path.isdir(settings.MEDIA_ROOT), "test" == settings.ENV]):
            shutil.rmtree(settings.MEDIA_ROOT)

    request.addfinalizer(fin)
