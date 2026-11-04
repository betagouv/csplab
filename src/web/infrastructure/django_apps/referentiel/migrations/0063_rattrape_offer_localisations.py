from django.db import migrations

# Copies the localisation stored in the flat columns of `offers` as the main
# localisation (position 0) of each offer. Plain SQL, like 0058, so that the
# migration does not depend on libs/referentiel.
RATTRAPE_OFFER_LOCALISATIONS = """
INSERT INTO offer_localisations (
    id, created_at, updated_at, offer_id, position,
    area, country, region, department, label, latitude, longitude
)
SELECT
    gen_random_uuid(), now(), now(), o.id, 0,
    o.area, o.country, o.region, o.department,
    coalesce(o.location_label, ''), o.latitude, o.longitude
FROM offers o
WHERE o.area IS NOT NULL
    AND o.country IS NOT NULL
    AND NOT EXISTS (
        SELECT 1 FROM offer_localisations ol WHERE ol.offer_id = o.id
    )
"""


class Migration(migrations.Migration):
    dependencies = [
        ("referentiel", "0062_offer_localisations"),
    ]

    operations = [
        migrations.RunSQL(
            sql=RATTRAPE_OFFER_LOCALISATIONS,
            reverse_sql="DELETE FROM offer_localisations",
        ),
    ]
