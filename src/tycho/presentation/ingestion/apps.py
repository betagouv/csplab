from django.apps import AppConfig


class IngestionPresentationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "presentation.ingestion"
    label = "presentation_ingestion"
