from datetime import date

from django.test import RequestFactory

from infrastructure.django_apps.commons.admin import stat_snapshot_list_view
from infrastructure.django_apps.commons.enums import Metric
from infrastructure.django_apps.commons.models import StatSnapshotModel
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)


def get(params=None):
    request = RequestFactory().get("/", params or {})
    user = UtilisateurDjangoFactory(is_staff=True, is_superuser=True)
    user.is_verified = lambda: True
    request.user = user
    return stat_snapshot_list_view(request)


def create_snapshots():
    for metric in Metric:
        StatSnapshotModel.objects.create(
            date=date(2026, 6, 30), metric_name=metric, metric_value=1
        )


def test_lists_snapshots_with_metric_label(db):
    create_snapshots()

    content = get().content.decode()

    assert "<td>Offres publiées (nb_offres_publiees)</td>" in content
    assert "<td>Offres archivées (nb_offres_archivees)</td>" in content


def test_filters_by_metric_name(db):
    create_snapshots()

    content = get({"metric_name": Metric.ARCHIVED_OFFERS}).content.decode()

    assert "<td>Offres archivées (nb_offres_archivees)</td>" in content
    assert "<td>Offres publiées (nb_offres_publiees)</td>" not in content
