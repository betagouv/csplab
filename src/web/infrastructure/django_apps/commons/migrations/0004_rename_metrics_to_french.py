from django.db import migrations

RENAMES = [
    ("nb_published_offers", "nb_offres_publiees"),
    ("nb_archived_offers", "nb_offres_archivees"),
]


def rename(apps, schema_editor, *, reverse: bool) -> None:
    StatSnapshotModel = apps.get_model("commons", "StatSnapshotModel")
    for old, new in RENAMES:
        source, target = (new, old) if reverse else (old, new)
        StatSnapshotModel.objects.filter(metric_name=source).update(metric_name=target)


def forwards(apps, schema_editor):
    rename(apps, schema_editor, reverse=False)


def backwards(apps, schema_editor):
    rename(apps, schema_editor, reverse=True)


class Migration(migrations.Migration):
    dependencies = [
        ("commons", "0003_auditloginlogmodel"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
