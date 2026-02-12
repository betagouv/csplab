"""Django admin configuration for candidate models."""

from django.contrib import admin

from infrastructure.django_apps.candidate.models.cv_metadata import CVMetadataModel


@admin.register(CVMetadataModel)
class CVMetadataAdmin(admin.ModelAdmin):
    """Admin configuration for CVMetadata model."""

    list_display = ("filename", "id", "created_at", "search_query")
    list_filter = ("created_at",)
    search_fields = ("filename", "id")
    readonly_fields = [f.name for f in CVMetadataModel._meta.get_fields()]
