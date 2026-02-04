"""Django settings for tycho project in dev mode."""

from config.settings.test import *  # noqa: F403

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "192.168.0.1", "0.0.0.0"]  # noqa S104

# placeholder for dev logger setup

# placeholder for django debug toolbar setup
