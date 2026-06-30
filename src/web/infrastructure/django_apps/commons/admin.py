from django.contrib import admin

from infrastructure.django_apps.commons.models import AuditLogModel, StatsHistoryModel
from infrastructure.django_apps.utils.admin import ReadOnlyAdminMixin


@admin.register(AuditLogModel)
class AuditLogAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = (
        "occurred_at",
        "utilisateur_id",
        "event_name",
        "ressource_kind",
        "ressource_id",
    )
    list_filter = (
        "event_name",
        "ressource_kind",
        "occurred_at",
    )
    search_fields = ("utilisateur_id", "ressource_id")


@admin.register(StatsHistoryModel)
class StatsHistoryAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("date", "metric_name", "metric_value", "created_at")
    list_filter = ("metric_name", "date")
    ordering = ("-date", "metric_name")
