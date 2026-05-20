from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ingestion", "0021_source"),
    ]

    operations = [
        migrations.AddField(
            model_name="sourcemodel",
            name="source_id",
            field=models.UUIDField(unique=True, null=True),
        ),
    ]
