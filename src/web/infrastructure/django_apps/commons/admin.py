from django.contrib import admin

from infrastructure.django_apps.commons.models import AuditLogModel, StatSnapshotModel
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


@admin.register(StatSnapshotModel)
class StatSnapshotAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = (
        "date",
        "metric_name",
        "metric_value",
    )
    list_filter = (
        "metric_name",
        "date",
    )
    search_fields = ("metric_name",)
