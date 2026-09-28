from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('referentiel', '0043_offermodel_talentsoft_organisme_entity_code'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                WITH cible AS (
                    SELECT
                        id,
                        verse || '-' || reference AS external_id,
                        COUNT(*) OVER (
                            PARTITION BY verse || '-' || reference
                        ) AS nb
                    FROM offers
                    WHERE verse IS NOT NULL
                        AND external_id <> verse || '-' || reference
                )
                UPDATE offers
                SET external_id = cible.external_id
                FROM cible
                WHERE offers.id = cible.id
                    AND cible.nb = 1
                    AND NOT EXISTS (
                        SELECT 1 FROM offers existante
                        WHERE existante.external_id = cible.external_id
                    )
            """,
            reverse_sql=migrations.RunSQL.noop,
            elidable=True,
        ),
    ]
