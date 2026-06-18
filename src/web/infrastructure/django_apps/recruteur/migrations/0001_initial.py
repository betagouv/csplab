import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="OrganismeModel",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("nom", models.CharField(max_length=255)),
                (
                    "versant",
                    models.CharField(
                        choices=[("FPT", "FPT"), ("FPE", "FPE"), ("FPH", "FPH")],
                        max_length=10,
                    ),
                ),
                (
                    "siret",
                    models.CharField(blank=True, max_length=14, null=True, unique=True),
                ),
                ("parent_id", models.UUIDField(blank=True, null=True)),
                ("localisation", models.JSONField(blank=True, null=True)),
            ],
            options={
                "verbose_name": "Organisme",
                "verbose_name_plural": "Organismes",
                "db_table": "organisme",
            },
        ),
    ]
