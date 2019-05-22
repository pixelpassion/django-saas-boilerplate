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
def test(
    c,
    recreate_test_db=False,
    verbose=True,
    pdb=False,
    failed_first=False,
    maxfail=9999,
    args="",
):
    """
    Runs the local backend unit tests with py.test.

    Supported arguments:
    -r, --recreate-test-db\n\tto (re)create and migrate the test DB;
    -v, --verbose\n\tto increase output verbosity;
    -p, --pdb\n\tto enter a PDB session to debug test failures;
    -f, --failed_first\n\tto run first the previously failed tests;
    -m, --maxfail=NUM\n\tto stop after NUM failures (default: 9999; 1=stop on fail);
    -a ARGS, --args=ARGS\n\tARGS to pass (default: empty)
    """

    if recreate_test_db:
        c.run("py.test -vv --create-db --migrations --no-cov -k 'test_dummy'")

    # Run all the tests and report coverage.
    c.run(
        "py.test {v} {p} {f} {m} {args}".format(
            v="-v" if verbose else "",
            p="--pdb" if pdb else "",
            m=f"--maxfail={maxfail}" if maxfail > 0 else "",
            f="--ff" if failed_first else "",
            args=args,
        )
    )


@task
def foreman(c):
    with tempfile.NamedTemporaryFile(mode="w") as f:
        f.write("DJANGO_SETTINGS_MODULE=conf.settings.local")
        f.flush()
        dotenv.load_dotenv()
        print(os.getenv("SECRET_KEY"))
        c.run('foreman start -e {}'.format(f.name))


@task
def circleci(c):
    c.run('circleci local execute', pty=True)