from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ingestion", "0020_alter_rawdocument_document_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="SourceModel",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("source_id", models.UUIDField(unique=True, null=True)),
                (
                    "type",
                    models.CharField(
                        choices=[("talentsoft", "talentsoft")],
                        max_length=50,
                    ),
                ),
                ("client_id_front", models.CharField(max_length=255)),
                ("client_id_back", models.CharField(max_length=255)),
                ("base_url", models.URLField(max_length=255)),
            ],
            options={
                "verbose_name": "Source",
                "verbose_name_plural": "Sources",
                "db_table": "source",
            },
        ),
    ]
