import os


def go_docker():
    os.system("docker-compose up -d")


def coverage_report():
    os.system("coverage run -m py.test")


def coverage_xml():
    os.system("coverage xml")


def check_coverage():
    os.system("coverage report --fail-under=95")
