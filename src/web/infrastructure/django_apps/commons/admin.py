from django.contrib import admin

from infrastructure.django_apps.commons.models import AuditLogModel
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
