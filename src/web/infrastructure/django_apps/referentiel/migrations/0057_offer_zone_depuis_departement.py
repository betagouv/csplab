from django.db import migrations

# Rattrape les offres Talentsoft publiées avant #2077 et #2097 : la zone est
# déduite du département (zone_pour_departement), la région des offres
# d'outre-mer est DOM ou TOM (overseas_region_for_department). Les
# correspondances sont figées ici pour ne pas dépendre de libs/referentiel.
RATTRAPE_LOCALISATION_TALENTSOFT = """
WITH localisation AS (
    SELECT
        o.id,
        CASE
            WHEN o.department IN ('971', '972', '973', '975', 'SPM') THEN 'AM'
            WHEN o.department IN ('974', '976') THEN 'AF'
            WHEN o.department IN ('986', '987', '988', 'WLF') THEN 'OC'
            ELSE 'EU'
        END AS area,
        CASE
            WHEN o.department IN ('971', '972', '973', '974', '976') THEN 'DOM'
            WHEN o.department IN ('975', '986', '987', '988', 'SPM', 'WLF')
                THEN 'TOM'
            ELSE o.region
        END AS region
    FROM offers o
    JOIN sources s ON s.source_id = o.source_id
    WHERE s.type = 'talentsoft'
        AND o.country IS NOT NULL
        AND o.region IS NOT NULL
        AND (
            o.department ~ '^(0[1-9]|1[0-9]|2[1-9AB]|[3-8][0-9]|9[0-5])$'
            OR o.department IN (
                '971', '972', '973', '974', '976',
                '975', '986', '987', '988', 'SPM', 'WLF'
            )
        )
)
UPDATE offers o
SET area = l.area, region = l.region
FROM localisation l
WHERE o.id = l.id
    AND (o.area IS DISTINCT FROM l.area OR o.region IS DISTINCT FROM l.region)
"""


class Migration(migrations.Migration):
    dependencies = [
        ("referentiel", "0056_offer_categories"),
    ]

    operations = [
        migrations.RunSQL(
            sql=RATTRAPE_LOCALISATION_TALENTSOFT,
            reverse_sql=migrations.RunSQL.noop,
            elidable=True,
        ),
    ]
