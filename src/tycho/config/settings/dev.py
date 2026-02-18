"""Django settings for tycho project in dev mode."""

from config.settings.base import *  # noqa: F403

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "192.168.0.1", "0.0.0.0"]  # noqa S104

# placeholder for dev logger setup

# Debug Toolbar Settings
INTERNAL_IPS = ["127.0.0.1"]

INSTALLED_APPS.extend(  # noqa: F405
    [
        "debug_toolbar",
    ]
)

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa F405

DEBUG_TOOLBAR_CONFIG = {
    # https://django-debug-toolbar.readthedocs.io/en/latest/panels.html#panels
    "DISABLE_PANELS": [
        "debug_toolbar.panels.redirects.RedirectsPanel",
        # ProfilingPanel makes the django admin extremely slow...
        "debug_toolbar.panels.profiling.ProfilingPanel",
    ],
    "SHOW_TEMPLATE_CONTEXT": True,
}

# Use simple static files storage for development (no compression/manifest)
STORAGES = {
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

SENTRY_DNS = "example.com"
