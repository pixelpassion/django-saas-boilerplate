import hashlib
import os

import pytest


@pytest.fixture
def remove_tempdir(request):
    """ This fixture remove temporary temprequirements.txt created for the
        test_requirements_circleci test.
    """

    def fin():
        os.remove("temprequirements.txt")

    request.addfinalizer(fin)


def test_requirements_circleci(remove_tempdir):
    """Test that generates temprequirements.txt file from pyproject.toml and
       checks if we have the same requirements in our project."""

    os.system("poetry export -f requirements.txt > temprequirements.txt")
    with open("requirements.txt", "r") as project_requirements, open(
        "temprequirements.txt", "r"
    ) as test_requirements:
        assert (
            hashlib.md5(project_requirements.read().encode("utf-8")).hexdigest()
            == hashlib.md5(test_requirements.read().encode("utf-8")).hexdigest()
        )
