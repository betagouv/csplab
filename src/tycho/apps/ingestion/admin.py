"""Django admin configuration for ingestion models."""

from django.contrib import admin

from apps.ingestion.infrastructure.adapters.persistence.models import RawDocument
from apps.ingestion.infrastructure.adapters.persistence.models.corps import CorpsModel


class RawDocumentAdmin(admin.ModelAdmin):
    """Admin interface for RawDocument model."""

    list_display = ("id", "document_type", "raw_data", "created_at", "updated_at")


class CorpsAdmin(admin.ModelAdmin):
    """Admin interface for Corps model."""

    list_display = (
        "id",
        "code",
        "short_label",
        "long_label",
        "category",
        "ministry",
        "diploma_level",
        "access_modalities",
    )
    list_filter = ("category", "ministry", "diploma_level")
    search_fields = ("code", "short_label", "long_label")
    readonly_fields = ("id", "created_at", "updated_at")

    fieldsets = (
        (
            "Informations générales",
            {"fields": ("id", "code", "short_label", "long_label")},
        ),
        ("Classification", {"fields": ("category", "ministry", "diploma_level")}),
        ("Modalités d'accès", {"fields": ("access_modalities",)}),
        (
            "Métadonnées",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


admin.site.register(RawDocument, RawDocumentAdmin)
admin.site.register(CorpsModel, CorpsAdmin)
