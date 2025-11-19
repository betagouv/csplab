"""Django admin configuration for ingestion models."""

from django.contrib import admin

from apps.ingestion.infrastructure.adapters.persistence.models import RawDocument


class RawDocumentAdmin(admin.ModelAdmin):
    """Admin interface for RawCorps model."""

    list_display = ("raw_data", "created_at", "updated_at")


admin.site.register(RawDocument, RawDocumentAdmin)
