from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ingestion", "0024_alter_sourcemodel_id_alter_sourcemodel_source_id"),
    ]

    operations = [
        migrations.RunSQL(
            elidable=True,
            sql=[
                """
                DELETE FROM ingestion_rawdocument
                WHERE id IN (
                    SELECT id
                    FROM (
                        SELECT id,
                               ROW_NUMBER() OVER (PARTITION BY external_id, document_type ORDER BY created_at DESC) AS rn
                        FROM ingestion_rawdocument
                    ) sub
                    WHERE rn > 1
                );
                """,
                "CREATE INDEX IF NOT EXISTS ingestion_rawdocument_externa_3ec9c2 ON ingestion_rawdocument(external_id);",
                "CREATE UNIQUE INDEX IF NOT EXISTS unique_external_id_document_type ON ingestion_rawdocument(external_id, document_type);",
            ],
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
