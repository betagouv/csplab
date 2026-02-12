"""Django admin configuration for ingestion models."""

from django.contrib import admin

from infrastructure.django_apps.ingestion.models.raw_document import RawDocument


@admin.register(RawDocument)
class RawDocumentAdmin(admin.ModelAdmin):
    """Admin interface for RawDocument model."""

    list_display = (
        "id",
        "external_id",
        "document_type",
        "created_at",
        "updated_at",
    )
    list_filter = ("document_type", "created_at", "updated_at")
    readonly_fields = [f.name for f in RawDocument._meta.get_fields()]
