from django.contrib import admin

from infrastructure.django_apps.commons.models import AuditLogModel


@admin.register(AuditLogModel)
class AuditLogAdmin(admin.ModelAdmin):
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
    readonly_fields = [f.name for f in AuditLogModel._meta.get_fields()]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
