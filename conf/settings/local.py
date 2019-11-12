from .base import *

INSTALLED_APPS = INSTALLED_APPS + ["django_werkzeug", "debug_toolbar"]

MIDDLEWARE = MIDDLEWARE + ["debug_toolbar.middleware.DebugToolbarMiddleware"]
