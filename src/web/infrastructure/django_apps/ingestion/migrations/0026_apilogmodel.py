from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ingestion", "0025_fix_missing_indexes"),
    ]

    operations = [
        migrations.CreateModel(
            name="ApiLogModel",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("timestamp", models.DateTimeField()),
                ("path", models.CharField(max_length=2048)),
                ("ip_address", models.GenericIPAddressField()),
                ("method", models.CharField(max_length=10)),
                ("status_code", models.PositiveSmallIntegerField()),
                ("auth_token", models.TextField(blank=True, null=True)),
                ("token_type", models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                "verbose_name": "API Log",
                "verbose_name_plural": "API Logs",
                "db_table": "api_logs",
                "indexes": [
                    models.Index(fields=["timestamp"], name="api_logs_timestamp_idx"),
                    models.Index(fields=["path"], name="api_logs_path_idx"),
                    models.Index(fields=["ip_address"], name="api_logs_ip_address_idx"),
                    models.Index(fields=["token_type"], name="api_logs_token_type_idx"),
                ],
            },
        ),
    ]
