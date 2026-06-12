import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "candidate",
            "0002_cvmetadatamodel_status_cvmetadatamodel_updated_at_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="CandidatureModel",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("candidat_id", models.UUIDField()),
                ("offre_id", models.UUIDField()),
                (
                    "statut",
                    models.CharField(
                        choices=[
                            ("initial", "initial"),
                            ("soumise", "soumise"),
                            ("retiree", "retiree"),
                        ],
                        default="initial",
                        max_length=20,
                    ),
                ),
                ("documents", models.JSONField(blank=True, null=True)),
                ("soumise_le", models.DateTimeField(blank=True, null=True)),
                ("mise_a_jour_le", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "verbose_name": "Candidature",
                "verbose_name_plural": "Candidatures",
                "db_table": "candidature",
                "constraints": [
                    models.UniqueConstraint(
                        fields=("candidat_id", "offre_id"),
                        name="unique_candidature_candidat_offre",
                    )
                ],
            },
        ),
    ]
