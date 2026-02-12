"""Django settings for tycho project."""

from datetime import timedelta
from pathlib import Path

import environ
import sentry_sdk
from django.utils.translation import gettext_lazy as _
from sentry_sdk.integrations.django import DjangoIntegration

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    TYCHO_ALLOWED_HOSTS=(list, ["localhost"]),
    TYCHO_LOG_LEVEL=(str, "INFO"),
    TYCHO_CSRF_TRUSTED_ORIGINS=(list, []),
    TYCHO_SENTRY_DSN=(str, ""),
    TYCHO_SENTRY_TRACES_SAMPLE_RATE=(float, 0.0),
    TYCHO_SENTRY_PROFILES_SAMPLE_RATE=(float, 0.0),
    TYCHO_PISTE_OAUTH_BASE_URL=(str, "https://fake-piste-oauth.example.com"),
    TYCHO_INGRES_BASE_URL=(str, "https://fake-ingres-api.example.com/path"),
    TYCHO_INGRES_CLIENT_ID=(str, "fake-client-id"),
    TYCHO_INGRES_CLIENT_SECRET=(str, "fake-client-secret"),
    TYCHO_OCR_TYPE=(str, "ALBERT"),
    TYCHO_OPENROUTER_API_KEY=(str, "fake-api-key"),
    TYCHO_OPENROUTER_BASE_URL=(str, "https://api.openai.com/v1"),
    TYCHO_OPENROUTER_EMBEDDING_MODEL=(str, "text-embedding-3-large"),
    TYCHO_OPENROUTER_OCR_MODEL=(str, "openai/gpt-5.2"),
    TYCHO_ALBERT_API_BASE_URL=(str, "https://albert.api.etalab.gouv.fr"),
    TYCHO_ALBERT_API_KEY=(str, "albert-api-key"),
    TYCHO_ALBERT_OCR_MODEL=(str, "albert-large"),
    TYCHO_ALBERT_OCR_DPI=(int, 200),
    TYCHO_OPIK_API_KEY=(str, "opik-api-key"),
    TYCHO_TALENTSOFT_CLIENT_ID=(str, "fake-client-id"),
    TYCHO_TALENTSOFT_CLIENT_SECRET=(str, "fake-client-secret"),
    TYCHO_TALENTSOFT_BASE_URL=(str, "https://fake-talentsoft.example.com"),
)
env.prefix = "TYCHO_"

DEBUG = False
SECRET_KEY = env.str("SECRET_KEY")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# CSRF trusted origins for HTTPS requests
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])


# Application definition


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "rest_framework",
    "rest_framework_simplejwt",
    "django_htmx",
    "dsfr",
    "infrastructure.django_apps.shared",
    "infrastructure.django_apps.ingestion",
    "infrastructure.django_apps.candidate",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "presentation" / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
                "django.contrib.messages.context_processors.messages",
                "dsfr.context_processors.site_config",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
DATABASES = {"default": env.db("DATABASE_URL")}


# Password validation
PASSWORD_MIN_LENGTH = 14
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"  # noqa E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": PASSWORD_MIN_LENGTH},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
LANGUAGE_CODE = "fr"
LANGUAGES = [
    ("fr", _("French")),
]
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
LOCALE_PATHS = [BASE_DIR / "locale"]

# Static files (CSS, JavaScript, Images)

# let whitenoise manage checksum integrity
DSFR_USE_INTEGRITY_CHECKSUMS = False

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static_collected"

STORAGES = {
    "staticfiles": {
        # TODO - reactivate Manifest
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Static files directory inside the package presentation app
STATIC_DIR = BASE_DIR / "presentation" / "static"
STATICFILES_DIRS = (STATIC_DIR,)

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Maximum CV size in cv upload flow
CV_MAX_SIZE_MB = 5

# Polling interval for CV processing status (in seconds)
CV_PROCESSING_POLL_INTERVAL = 2

# Logging configuration
LOG_LEVEL = env.str("LOG_LEVEL")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} [{name}] {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "exception_console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "ingestion": {
            "handlers": ["exception_console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "candidate": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "tycho": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
}

# Django REST Framework
REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "config.exception_handler.custom_exception_handler",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 100,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

# Sentry
sentry_sdk.init(
    dsn=env.str("SENTRY_DSN"),
    integrations=[DjangoIntegration()],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=env.float("SENTRY_TRACES_SAMPLE_RATE"),
    # To set a uniform sample rate
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production
    profiles_sample_rate=env.float("SENTRY_PROFILES_SAMPLE_RATE"),
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)

# API endpoints
PISTE_OAUTH_BASE_URL = env.str("PISTE_OAUTH_BASE_URL")

INGRES_BASE_URL = env.str("INGRES_BASE_URL")
INGRES_CLIENT_ID = env.str("INGRES_CLIENT_ID")
INGRES_CLIENT_SECRET = env.str("INGRES_CLIENT_SECRET")

OCR_TYPE = env.str("OCR_TYPE")

OPENROUTER_BASE_URL = env.str("OPENROUTER_BASE_URL")
OPENROUTER_API_KEY = env.str("OPENROUTER_API_KEY")
OPENROUTER_EMBEDDING_MODEL = env.str("OPENROUTER_EMBEDDING_MODEL")
OPENROUTER_OCR_MODEL = env.str("OPENROUTER_OCR_MODEL")

ALBERT_API_BASE_URL = env.str("ALBERT_API_BASE_URL")
ALBERT_API_KEY = env.str("ALBERT_API_KEY")
ALBERT_OCR_MODEL = env.str("ALBERT_OCR_MODEL")
ALBERT_OCR_DPI = env.str("ALBERT_OCR_DPI")

OPIK_API_KEY = env.str("OPIK_API_KEY")

TALENTSOFT_BASE_URL = env.str("TALENTSOFT_BASE_URL")
TALENTSOFT_CLIENT_ID = env.str("TALENTSOFT_CLIENT_ID")
TALENTSOFT_CLIENT_SECRET = env.str("TALENTSOFT_CLIENT_SECRET")
