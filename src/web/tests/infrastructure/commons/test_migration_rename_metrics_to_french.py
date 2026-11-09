# TODO: remove after PR#2338 is merged
from datetime import date

import pytest
from django.db import connection
from django.db.migrations.executor import MigrationExecutor

BEFORE = ("commons", "0003_auditloginlogmodel")
AFTER = ("commons", "0004_rename_metrics_to_french")


def migrate_to(target):
    executor = MigrationExecutor(connection)
    executor.loader.build_graph()
    executor.migrate([target])
    return executor.loader.project_state([target]).apps


@pytest.mark.django_db(transaction=True)
def test_renames_metrics_and_reverts():
    apps = migrate_to(BEFORE)
    snapshot_model = apps.get_model("commons", "StatSnapshotModel")
    snapshot_model.objects.create(
        date=date(2026, 6, 30), metric_name="nb_published_offers", metric_value=3
    )
    snapshot_model.objects.create(
        date=date(2026, 6, 30), metric_name="nb_archived_offers", metric_value=2
    )

    apps = migrate_to(AFTER)
    names = set(
        apps.get_model("commons", "StatSnapshotModel").objects.values_list(
            "metric_name", flat=True
        )
    )
    assert names == {"nb_offres_publiees", "nb_offres_archivees"}

    apps = migrate_to(BEFORE)
    names = set(
        apps.get_model("commons", "StatSnapshotModel").objects.values_list(
            "metric_name", flat=True
        )
    )
    assert names == {"nb_published_offers", "nb_archived_offers"}

    migrate_to(AFTER)
