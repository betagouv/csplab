from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recruteur", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="OrganismeModel",
            name="etapes",
            field=models.JSONField(
                blank=True,
                null=True,
                help_text=(
                    "Ordered recruitment steps. "
                    "Each item: {'entity_id': str, 'categorie': str, 'nom': str}"
                ),
            ),
        ),
    ]
