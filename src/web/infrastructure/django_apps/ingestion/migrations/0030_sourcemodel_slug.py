from django.db import migrations, models


def backfill_slug(apps, schema_editor):
    SourceModel = apps.get_model("ingestion", "SourceModel")
    SourceModel.objects.filter(slug__isnull=True).update(slug="talentsoft-main")


class Migration(migrations.Migration):
    dependencies = [
        ("ingestion", "0029_fix_rawdocument_id_index"),
    ]

    operations = [
        migrations.AddField(
            model_name="sourcemodel",
            name="slug",
            field=models.SlugField(max_length=255, null=True),
        ),
        migrations.RunPython(backfill_slug, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="sourcemodel",
            name="slug",
            field=models.SlugField(max_length=255),
        ),
    ]
