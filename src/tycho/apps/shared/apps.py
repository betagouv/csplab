"""Django app configuration for shared module."""

from django.apps import AppConfig


class SharedConfig(AppConfig):
    """Configuration for the shared Django app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.shared"
