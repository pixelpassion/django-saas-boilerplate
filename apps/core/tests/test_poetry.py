import hashlib
import os


def test_requirements_circleci():
    """Test that generates temprequirements.txt file from pyproject.toml and
       checks if we have the same requirements in our project."""

    os.system("poetry export -f requirements.txt > temprequirements.txt")
    project_requirements = open("requirements.txt", "r")
    test_requirements = open("temprequirements.txt", "r")
    assert (
        hashlib.md5(project_requirements.read().encode("utf-8")).hexdigest()
        == hashlib.md5(test_requirements.read().encode("utf-8")).hexdigest()
    )
    os.remove("temprequirements.txt")
