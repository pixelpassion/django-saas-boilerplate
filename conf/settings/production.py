import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *


RAVEN_CONFIG = {"dsn": env("SENTRY_DSN"), "integrations": [DjangoIntegration()]}
SENTRY_PROJECT_NAME = env("SENTRY_PROJECT_NAME", default="project_name")
RAVEN_CONFIG["release"] = f"{SENTRY_PROJECT_NAME}-{HEROKU_SLUG_COMMIT}"
sentry_sdk.init(**RAVEN_CONFIG)
