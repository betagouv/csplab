from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("commons", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="StatsHistoryModel",
            fields=[
                (
                    "id",
                    models.UUIDField(primary_key=True, serialize=False),
                ),
                ("date", models.DateField()),
                ("metric_name", models.CharField(max_length=255)),
                ("metric_value", models.BigIntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Stats History",
                "verbose_name_plural": "Stats History",
                "db_table": "stats_history",
                "ordering": ["-date"],
            },
        ),
        migrations.AddConstraint(
            model_name="statshistorymodel",
            constraint=models.UniqueConstraint(
                fields=["date", "metric_name"],
                name="unique_stats_history_date_metric_name",
            ),
        ),
    ]
