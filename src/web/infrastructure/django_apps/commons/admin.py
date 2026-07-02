from typing import Any

from django.contrib import admin
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse

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


def stat_snapshot_list_view(request: HttpRequest) -> HttpResponse:
    """Read-only listing for StatSnapshotModel.

    StatSnapshotModel has a composite primary key, which Django admin
    refuses to register directly (ImproperlyConfigured), so this view
    stands in for a ModelAdmin.
    """
    queryset = StatSnapshotModel.objects.all()
    metric_names = list(
        StatSnapshotModel.objects.order_by("metric_name")
        .values_list("metric_name", flat=True)
        .distinct()
    )

    selected_metric_name = request.GET.get("metric_name", "")
    if selected_metric_name:
        queryset = queryset.filter(metric_name=selected_metric_name)

    page = Paginator(queryset, 100).get_page(request.GET.get("page"))

    context = {
        **admin.site.each_context(request),
        "title": "Stat Snapshots",
        "page_obj": page,
        "metric_names": metric_names,
        "selected_metric_name": selected_metric_name,
    }
    return render(request, "admin/commons/stat_snapshot_list.html", context)


def _register_stat_snapshot_admin_link() -> None:
    """Surface stat_snapshot_list_view on the /admin index, in the Commons block.

    StatSnapshotModel can't be admin.site.register()-ed (composite primary
    key), so there is no ModelAdmin to generate the usual index entry.
    """
    original_get_app_list = admin.site.get_app_list

    def get_app_list_with_stat_snapshots(
        request: HttpRequest, app_label: str | None = None
    ) -> list[dict[str, Any]]:
        app_list = original_get_app_list(request, app_label=app_label)
        for app in app_list:
            if app["app_label"] == "commons":
                app["models"].append(
                    {
                        "name": "Stat Snapshots",
                        "object_name": "StatSnapshot",
                        "perms": {"view": True},
                        "admin_url": reverse("admin_stat_snapshot_list"),
                        "add_url": None,
                        "view_only": True,
                    }
                )
        return app_list

    admin.site.get_app_list = get_app_list_with_stat_snapshots  # type: ignore[method-assign]


_register_stat_snapshot_admin_link()
