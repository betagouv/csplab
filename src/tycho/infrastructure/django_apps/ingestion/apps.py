"""Django app configuration for ingestion module."""

from django.apps import AppConfig


class IngestionConfig(AppConfig):
    """Configuration for the ingestion Django app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "infrastructure.django_apps.ingestion"
