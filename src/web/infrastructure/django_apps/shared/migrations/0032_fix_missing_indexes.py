from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shared", "0031_offermodel_reference"),
    ]

    operations = [
        migrations.RunSQL(
            elidable=True,
            sql=[
                """
                DELETE FROM offers
                WHERE id IN (
                    SELECT id
                    FROM (
                        SELECT id,
                               ROW_NUMBER() OVER (PARTITION BY external_id ORDER BY created_at DESC) AS rn
                        FROM offers
                    ) sub
                    WHERE rn > 1
                );
                """,
                "CREATE UNIQUE INDEX IF NOT EXISTS offers_externa_40a57b_uniq ON offers(external_id);",
                "CREATE INDEX IF NOT EXISTS offers_externa_91aec4_idx ON offers(external_id);",
                "CREATE INDEX IF NOT EXISTS concours_nor_ori_fd92de_idx ON concours(nor_original);",
                "CREATE UNIQUE INDEX IF NOT EXISTS metiers_externa_467155_uniq ON metiers(external_id);",
                "CREATE INDEX IF NOT EXISTS metiers_externa_310f85_idx ON metiers(external_id);",
            ],
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
