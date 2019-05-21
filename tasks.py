import platform

from invoke import task


IS_WINDOWS = platform.system() == "Windows"

PTY = not IS_WINDOWS


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
        c.run("py.test -vv --create-db --migrations --no-cov -k 'test_dummy'", pty=PTY)

    # Run all the tests and report coverage.
    c.run(
        "py.test {v} {p} {f} {m} {args}".format(
            v="-v" if verbose else "",
            p="--pdb" if pdb else "",
            m=f"--maxfail={maxfail}" if maxfail > 0 else "",
            f="--ff" if failed_first else "",
            args=args,
        ),
        pty=PTY,
    )

    # Remove any email attachments created during the test run.
    run_django_code(
        c,
        """
import os, shutil
shutil.rmtree(os.path.join('_media', 'email-attachments'), ignore_errors=True)
        """,
    )
