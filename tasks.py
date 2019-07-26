import os
import tempfile

import dotenv
from invoke import task


@task
def db(c):
    c.run("docker-compose up -d postgres redis", pty=True)


@task
def create_admin(c):
    import django

    os.environ["DJANGO_SETTINGS_MODULE"] = "conf.settings.local"
    django.setup()
    from django.contrib.auth.models import User

    User.objects.create_superuser(
        os.getenv("ADMIN_LOGIN"), os.getenv("ADMIN_EMAIL"), os.getenv("ADMIN_PASSWORD")
    )


@task
def runserver(c):
    c.run("python manage.py runserver_plus", pty=True)


@task
def test(c,):
    """
    Runs the local backend unit tests with py.test.

    """
    # Run all the tests and report coverage.
    c.run("pipenv run create-coverage")

    # Check that test coverage is bigger than required percent
    c.run("pipenv run show-coverage")


@task
def foreman(c):
    with tempfile.NamedTemporaryFile(mode="w") as f:
        f.write("DJANGO_SETTINGS_MODULE=conf.settings.local")
        f.flush()
        dotenv.load_dotenv()
        print(os.getenv("SECRET_KEY"))
        c.run("foreman start -e {}".format(f.name))


@task
def circleci(c):
    c.run("circleci local execute", pty=True)

