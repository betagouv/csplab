from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ingestion", "0021_source"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="sourcemodel",
            name="base_url",
        ),
        migrations.AddField(
            model_name="sourcemodel",
            name="base_url_front",
            field=models.URLField(default=""),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="sourcemodel",
            name="base_url_back",
            field=models.URLField(default=""),
            preserve_default=False,
        ),
    ]
