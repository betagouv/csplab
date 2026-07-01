from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("commons", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="StatSnapshotModel",
            fields=[
                ("pk", models.CompositePrimaryKey("date", "metric_name", blank=True, editable=False, primary_key=True, serialize=False)),
                ("date", models.DateField()),
                ("metric_name", models.CharField(max_length=255)),
                ("metric_value", models.BigIntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Stat Snapshot",
                "verbose_name_plural": "Stat Snapshots",
                "db_table": "stat_snapshots",
                "ordering": ["-date"],
            },
        ),
    ]
