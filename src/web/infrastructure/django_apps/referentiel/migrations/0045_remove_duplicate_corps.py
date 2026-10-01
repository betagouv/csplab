from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('referentiel', '0044_normalize_offer_external_id'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                DELETE FROM corps
                WHERE id IN (
                    SELECT id FROM (
                        SELECT
                            id,
                            ROW_NUMBER() OVER (
                                PARTITION BY code
                                ORDER BY processed_at DESC NULLS LAST, created_at, id
                            ) AS rang
                        FROM corps
                    ) doublons
                    WHERE rang > 1
                )
            """,
            reverse_sql=migrations.RunSQL.noop,
            elidable=True,
        ),
    ]
