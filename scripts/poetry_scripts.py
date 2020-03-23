import os


def go_docker():
    """Script for starting the containers in the background and leaving them running."""
    os.system("docker-compose up -d")


def coverage_report():
    """Script for running coverage tests."""
    os.system("coverage run -m py.test")


def coverage_xml():
    """Script for creating xml report on coverage."""
    os.system("coverage xml")


def check_coverage():
    """Script for creating coverage report."""
    os.system("coverage report --fail-under=95")


def generate_requirements():
    """Script for generating requirements.txt from pyproject.toml"""
    os.system("poetry export -f requirements.txt > requirements.txt")
