"""
Base settings. Please do not modify this file
"""
import sys

import warnings
from pathlib import Path

import sentry_sdk
from django.utils.translation import gettext_lazy as _

import environ

# Build paths inside the project like this: BASE_DIR / "foo" / "bar"
from sentry_sdk.integrations.django import DjangoIntegration

PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()

env = environ.Env()

ENV_NOT_FOUND = False
with warnings.catch_warnings():
    try:
        warnings.simplefilter("error", Warning)
        environ.Env.read_env(env("PIPENV_DOTENV_LOCATION", default=str(PROJECT_ROOT / ".env")))
    except Warning:
        ENV_NOT_FOUND = True

STAGE = env.str("STAGE")
API_DOCS_ENABLED = env.bool("API_DOCS_ENABLED", default=STAGE != "production")

if ENV_NOT_FOUND is True and STAGE != "production":
    print("**** No .env found - this can be ignored on production ****", file=sys.stderr)

SECRET_KEY = env("SECRET_KEY", default="notsafeforproduction")
DEBUG = env.bool("DEBUG", default=STAGE != "production")
APPEND_SLASH = True
SITE_ID = 1


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.redirects",
    "django.contrib.postgres",
    "rest_framework",
    "apps.core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "conf.urls"

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [str(PROJECT_ROOT / "templates")],
    "APP_DIRS": True,
    "OPTIONS": {
        "context_processors": [
            "django.template.context_processors.debug",
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
        ],
        "string_if_invalid": "{%s is missing}",
        "debug": DEBUG,
    },
    "NAME": "django",
}]

STATIC_URL = '/static/'

WSGI_APPLICATION = "conf.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Language and locale

LANGUAGE_CODE = "en"

LANGUAGES = [("en", _("English")), ("de", _("German"))]

TIME_ZONE = "Europe/Berlin"

USE_I18N = True
USE_L10N = False  # If True, messes up dates / numbers format for the API!
USE_TZ = True

# This is necessary to be able to have custom Formats together with LANGUAGES
USE_THOUSAND_SEPARATOR = True

FORMAT_MODULE_PATH = (str(PROJECT_ROOT / "locale"),)

LOCALE_PATHS = FORMAT_MODULE_PATH

USE_SENDGRID = env("USE_SENDGRID", default=True)

HEROKU_SLUG_COMMIT = env("HEROKU_SLUG_COMMIT", default="nohash")[:8]


