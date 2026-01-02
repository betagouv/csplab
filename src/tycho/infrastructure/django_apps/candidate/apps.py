"""Django app configuration for candidate module."""

from django.apps import AppConfig


class CandidateConfig(AppConfig):
    """Configuration for the candidate Django app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "infrastructure.django_apps.candidate"
