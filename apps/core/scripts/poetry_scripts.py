import os


def coverage_report():
    os.system("coverage run -m py.test")


def coverage_xml():
    os.system("coverage xml")
