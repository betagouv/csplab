from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('referentiel', '0058_offer_zone_depuis_departement'),
    ]

    # Deletes the offers without category, active or archived, now rejected by
    # the API (article D.311-8 of the CGFP), see
    # https://github.com/betagouv/csplab/issues/2142. An offer turned into a
    # recrutement is kept: its foreign key is protected.
    operations = [
        migrations.RunSQL(
            sql="""
                DELETE FROM offers
                WHERE cardinality(offers.categories) = 0
                    AND NOT EXISTS (
                        SELECT 1 FROM recrutement WHERE recrutement.id = offers.id
                    )
            """,
            reverse_sql=migrations.RunSQL.noop,
            elidable=True,
        ),
    ]
