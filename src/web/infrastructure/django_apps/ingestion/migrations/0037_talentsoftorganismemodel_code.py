from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ingestion", "0036_purge_talentsoftorganismemodel"),
    ]

    operations = [
        migrations.AddField(
            model_name="talentsoftorganismemodel",
            name="code",
            field=models.IntegerField(unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="talentsoftorganismemodel",
            name="parent_code",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
