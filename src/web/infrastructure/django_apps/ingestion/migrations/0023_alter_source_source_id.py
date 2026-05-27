from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ingestion", "0022_alter_source_base_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sourcemodel",
            name="source_id",
            field=models.UUIDField(unique=True),
        ),
        migrations.AlterModelTable(
            name="sourcemodel",
            table="sources",
        ),
    ]
