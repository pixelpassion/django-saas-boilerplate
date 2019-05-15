from .base import *


CELERY_TASK_ALWAYS_EAGER = env.bool("CELERY_TASK_ALWAYS_EAGER", default=True)


INSTALLED_APPS = INSTALLED_APPS + [
    'django_werkzeug',
    'debug_toolbar',
]