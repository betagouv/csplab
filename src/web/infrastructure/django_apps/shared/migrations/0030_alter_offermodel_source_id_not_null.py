import django.db.models.deletion
from django.db import migrations, models


def hydrate_source(apps, schema_editor):
    OfferModel = apps.get_model("shared", "OfferModel")
    SourceModel = apps.get_model("ingestion", "SourceModel")
    source = SourceModel.objects.first()
    if source:
        OfferModel.objects.update(source=source)


class Migration(migrations.Migration):

    dependencies = [
        ("ingestion", "0024_alter_sourcemodel_id_alter_sourcemodel_source_id"),
        ("shared", "0029_populate_offer_source_id"),
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
        migrations.RunPython(hydrate_source, reverse_code=migrations.RunPython.noop),
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
        migrations.AddIndex(
            model_name="offermodel",
            index=models.Index(fields=["source"], name="offers_source_id_idx"),
        ),
    ]
