from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("ingestion", "0028_sourcemodel_created_at_sourcemodel_updated_at_and_more"),
    ]

    operations = [
        migrations.RunSQL(
            sql="CREATE UNIQUE INDEX IF NOT EXISTS ingestion_rawdocument_id_unique ON ingestion_rawdocument(id);",
        ),
    ]
