from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ingestion", "0024_alter_sourcemodel_id_alter_sourcemodel_source_id"),
        ("shared", "0029_populate_offer_source_id"),
    ]

    operations = [
        migrations.RunSQL(
            sql="UPDATE offers SET source_id = (SELECT source_id FROM sources LIMIT 1) WHERE source_id IS NULL",
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql="""
                        ALTER TABLE offers ALTER COLUMN source_id SET NOT NULL;
                        ALTER TABLE offers ADD CONSTRAINT offers_source_id_fk
                            FOREIGN KEY (source_id) REFERENCES sources(source_id);
                    """,
                    reverse_sql="""
                        ALTER TABLE offers DROP CONSTRAINT offers_source_id_fk;
                        ALTER TABLE offers ALTER COLUMN source_id DROP NOT NULL;
                    """,
                ),
            ],
            state_operations=[
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
                        db_column="source_id",
                        on_delete=models.PROTECT,
                        related_name="offers",
                        to="ingestion.sourcemodel",
                        to_field="source_id",
                    ),
                ),
                migrations.AddIndex(
                    model_name="offermodel",
                    index=models.Index(
                        fields=["source"], name="offers_source_id_idx"
                    ),
                ),
            ],
        ),
    ]
