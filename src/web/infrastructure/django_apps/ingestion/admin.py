"""Django admin configuration for ingestion models."""

from django.contrib import admin

from infrastructure.django_apps.ingestion.models.raw_document import RawDocument
from infrastructure.django_apps.ingestion.models.source import SourceModel


@admin.register(SourceModel)
class SourceAdmin(admin.ModelAdmin):
    list_display = (
        "source_id",
        "type",
        "base_url_front",
        "base_url_back",
        "client_id_front",
        "client_id_back",
    )
    list_filter = ("type",)
    search_fields = (
        "source_id",
        "base_url_front",
        "base_url_back",
        "client_id_front",
        "client_id_back",
    )
    readonly_fields = ("id", "source_id")


@admin.register(RawDocument)
class RawDocumentAdmin(admin.ModelAdmin):
    """Admin interface for RawDocument model."""

    list_display = (
        "external_id",
        "document_type",
        "updated_at",
        "processed_at",
        "error_msg",
    )
    list_filter = (
        "document_type",
        "created_at",
        "updated_at",
        "processed_at",
        ("error_msg", admin.EmptyFieldListFilter),
    )
    search_fields = ("external_id", "raw_data", "error_msg")
    readonly_fields = [f.name for f in RawDocument._meta.get_fields()]
