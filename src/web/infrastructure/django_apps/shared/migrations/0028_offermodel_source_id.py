from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "shared",
            "0027_rename_code_domaine_fonctionnel_metiermodel_domaine_fonctionnel_code",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="offermodel",
            name="source_id",
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AddIndex(
            model_name="offermodel",
            index=models.Index(fields=["source_id"], name="offers_source_id_idx"),
        ),
    ]
