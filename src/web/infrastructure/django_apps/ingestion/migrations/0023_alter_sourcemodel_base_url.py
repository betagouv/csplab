from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ingestion", "0022_sourcemodel_source_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sourcemodel",
            name="base_url",
            field=models.URLField(max_length=255),
        ),
    ]
