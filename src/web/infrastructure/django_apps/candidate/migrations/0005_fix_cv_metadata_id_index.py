from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("candidate", "0004_candidaturemodel"),
    ]

    operations = [
        migrations.RunSQL(
            sql="CREATE UNIQUE INDEX IF NOT EXISTS cv_metadata_id_unique ON cv_metadata(id);",
        ),
    ]
