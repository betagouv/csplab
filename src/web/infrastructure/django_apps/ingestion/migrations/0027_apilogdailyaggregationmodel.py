from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ingestion", "0026_apilogmodel"),
    ]

    operations = [
        migrations.CreateModel(
            name="ApiLogDailyAggregationModel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField()),
                ("method", models.CharField(max_length=10)),
                ("path", models.CharField(max_length=2048)),
                ("token_type", models.CharField(blank=True, max_length=20, null=True)),
                ("count", models.PositiveIntegerField()),
            ],
            options={
                "verbose_name": "API Log Daily Aggregation",
                "verbose_name_plural": "API Log Daily Aggregations",
                "db_table": "api_logs_daily_aggregations",
            },
        ),
        migrations.AddConstraint(
            model_name="ApiLogDailyAggregationModel",
            constraint=models.UniqueConstraint(
                fields=["date", "method", "path", "token_type"],
                name="api_logs_daily_agg_unique",
            ),
        ),
        migrations.AddIndex(
            model_name="ApiLogDailyAggregationModel",
            index=models.Index(fields=["date"], name="api_logs_daily_agg_date_idx"),
        ),
    ]
