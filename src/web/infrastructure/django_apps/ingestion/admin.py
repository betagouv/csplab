"""Django admin configuration for ingestion models."""

from django.contrib import admin

from infrastructure.django_apps.ingestion.models.api_log import ApiLogModel
from infrastructure.django_apps.ingestion.models.api_log_daily_aggregation import (
    ApiLogDailyAggregationModel,
)
from infrastructure.django_apps.ingestion.models.raw_document import RawDocument
from infrastructure.django_apps.ingestion.models.source import SourceModel


@admin.register(ApiLogModel)
class ApiLogAdmin(admin.ModelAdmin):
    list_display = (
        "timestamp",
        "method",
        "path",
        "status_code",
        "ip_address",
        "token_type",
    )
    list_filter = (
        "method",
        "status_code",
        "token_type",
        "timestamp",
    )
    search_fields = ("path", "ip_address", "auth_token")
    readonly_fields = [f.name for f in ApiLogModel._meta.get_fields()]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ApiLogDailyAggregationModel)
class ApiLogDailyAggregationAdmin(admin.ModelAdmin):
    list_display = ("date", "method", "path", "token_type", "count")
    list_filter = ("date", "method", "token_type")
    search_fields = ("path",)
    readonly_fields = [f.name for f in ApiLogDailyAggregationModel._meta.get_fields()]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SourceModel)
class SourceAdmin(admin.ModelAdmin):
    list_display = (
        "source_id",
        "slug",
        "type",
        "base_url_front",
        "base_url_back",
        "client_id_front",
        "client_id_back",
    )
    list_filter = ("type",)
    search_fields = (
        "source_id",
        "slug",
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
