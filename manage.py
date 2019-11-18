#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
    # Avoid the use of "python manage.py test", we are using py.test for testing
    if sys.argv[0] == "manage.py" and sys.argv[1] == "test":
        print("TESTING is only supported with py.test!")
        sys.exit(-1)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
