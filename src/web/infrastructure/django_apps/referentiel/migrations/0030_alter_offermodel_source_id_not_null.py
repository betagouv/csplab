import django.db.models.deletion
from django.db import migrations, models


def hydrate_source(apps, schema_editor):
    OfferModel = apps.get_model("referentiel", "OfferModel")
    SourceModel = apps.get_model("ingestion", "SourceModel")
    source = SourceModel.objects.first()
    if source:
        OfferModel.objects.update(source=source)


class Migration(migrations.Migration):
    replaces = [("shared", "0030_alter_offermodel_source_id_not_null")]

    dependencies = [
        ("ingestion", "0024_alter_sourcemodel_id_alter_sourcemodel_source_id"),
        ("referentiel", "0029_populate_offer_source_id"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="offermodel",
            name="offers_source_id_idx",
        ),
        migrations.RemoveField(
            model_name="offermodel",
            name="source_id",
        ),
        migrations.AddField(
            model_name="offermodel",
            name="source",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="offers",
                to="ingestion.sourcemodel",
                to_field="source_id",
            ),
        ),
        migrations.RunPython(hydrate_source, reverse_code=migrations.RunPython.noop, elidable=True),
        migrations.AlterField(
            model_name="offermodel",
            name="source",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="offers",
                to="ingestion.sourcemodel",
                to_field="source_id",
            ),
        ),
    ]
