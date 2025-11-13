"""Django admin configuration for ingestion models."""

from django.contrib import admin

from ingestion.models import RawCorps, RawExamination


class RawExaminationAdmin(admin.ModelAdmin):
    """Admin interface for RawExamination model."""

    list_display = ("nor", "legitext_id", "title", "created_at", "updated_at")


class RawCorpsAdmin(admin.ModelAdmin):
    """Admin interface for RawExamination model."""

    list_display = ("raw_data", "created_at", "updated_at")


admin.site.register(RawExamination, RawExaminationAdmin)
admin.site.register(RawCorps, RawCorpsAdmin)
