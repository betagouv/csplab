"""Django admin configuration for candidate models."""

from django.contrib import admin

from infrastructure.django_apps.candidate.models.cv_metadata import CVMetadataModel


class CVMetadataAdmin(admin.ModelAdmin):
    """Admin configuration for CVMetadata model."""

    list_display = ("filename", "id", "created_at", "extracted_text", "search_query")
    list_filter = ("created_at",)
    search_fields = ("filename", "id")


admin.site.register(CVMetadataModel, CVMetadataAdmin)
