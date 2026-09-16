from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("candidate", "0009_alter_candidaturemodel_candidat"),
    ]

    operations = [
        migrations.AddField(
            model_name="candidaturemodel",
            name="motif_refus",
            field=models.CharField(
                blank=True,
                choices=[
                    ("corps_grade_non_eligible", "Corps ou grade non éligible"),
                    (
                        "condition_mobilite_non_remplie",
                        "Condition de mobilité non remplie",
                    ),
                    ("candidat_non_fonctionnaire", "Candidat non fonctionnaire"),
                    ("experience_insuffisante", "Expérience insuffisante"),
                    (
                        "competences_techniques_insuffisantes",
                        "Compétences techniques insuffisantes",
                    ),
                    (
                        "niveau_qualification_insuffisant",
                        "Niveau de qualification insuffisant",
                    ),
                    ("disponibilite", "Disponibilité"),
                    ("autre", "Autre"),
                ],
                max_length=50,
                null=True,
            ),
        ),
    ]
