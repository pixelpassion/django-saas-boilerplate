from scripts.poetry_scripts import (
    check_coverage,
    coverage_report,
    coverage_xml,
    generate_requirements,
    go_docker,
)


def test_go_docker(mocker):
    """Test go_docker function from scripts.poetry_scripts"""
    mocked_function = mocker.patch("os.system")
    go_docker()
    mocked_function.assert_called_once_with("docker-compose up -d")


def test_coverage_report(mocker):
    """Test coverage_report function from scripts.poetry_scripts"""
    mocked_function = mocker.patch("os.system")
    coverage_report()
    mocked_function.assert_called_once_with("coverage run -m py.test")


def test_coverage_xml(mocker):
    """Test coverage_xml function from scripts.poetry_scripts"""
    mocked_function = mocker.patch("os.system")
    coverage_xml()
    mocked_function.assert_called_once_with("coverage xml")


def test_check_coverage(mocker):
    """Test check_coverage function from scripts.poetry_scripts"""
    mocked_function = mocker.patch("os.system")
    check_coverage()
    mocked_function.assert_called_once_with("coverage report --fail-under=95")


def test_generate_requirements(mocker):
    """Test check_coverage function from scripts.poetry_scripts"""
    mocked_function = mocker.patch("os.system")
    generate_requirements()
    mocked_function.assert_called_once_with(
        "poetry export -f requirements.txt > requirements.txt"
    )
