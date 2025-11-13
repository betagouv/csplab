"""Django admin configuration for ingestion models."""

from django.contrib import admin

from ingestion.models import RawExamination


class RawExaminationAdmin(admin.ModelAdmin):
    """Admin interface for RawExamination model."""

    list_display = ("nor", "legitext_id")  # Fields to display in admin list


admin.site.register(RawExamination, RawExaminationAdmin)
