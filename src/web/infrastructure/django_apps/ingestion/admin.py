"""Django admin configuration for ingestion models."""

from django.contrib import admin

from infrastructure.django_apps.ingestion.models.api_log import ApiLogModel
from infrastructure.django_apps.ingestion.models.api_log_daily_aggregation import (
    ApiLogDailyAggregationModel,
)
from infrastructure.django_apps.ingestion.models.raw_document import RawDocument
from infrastructure.django_apps.ingestion.models.source import SourceModel
from infrastructure.django_apps.utils.admin import ReadOnlyAdminMixin


@admin.register(ApiLogModel)
class ApiLogAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
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


@admin.register(ApiLogDailyAggregationModel)
class ApiLogDailyAggregationAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("date", "method", "path", "token_type", "count")
    list_filter = ("date", "method", "token_type")
    search_fields = ("path",)


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

    def save_model(self, request, obj, form, change):
        # enforce the entity invariants (__post_init__) before persisting
        obj.to_entity()
        super().save_model(request, obj, form, change)


@admin.register(RawDocument)
class RawDocumentAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
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
