from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('referentiel', '0055_metiers_offer_family_code_not_empty'),
    ]

    # Realigns the functional area of offers written before the ingestion fix
    # for the ER prefix (https://github.com/betagouv/csplab/pull/1096), see
    # https://github.com/betagouv/csplab/issues/2110. A metier with a single
    # domain imposes it; a metier with several domains takes the one following
    # the ER prefix.
    operations = [
        migrations.RunSQL(
            sql="""
                WITH metier_domaines AS (
                    SELECT
                        offer_family_code,
                        array_agg(DISTINCT domaine_fonctionnel_code) AS domaines
                    FROM metiers
                    GROUP BY offer_family_code
                ),
                domaines_cibles AS (
                    SELECT
                        offers.id,
                        CASE
                            WHEN cardinality(metier_domaines.domaines) = 1
                                THEN metier_domaines.domaines[1]
                            WHEN SUBSTRING(offers.code_emploi_csp FROM 3 FOR 3)
                                = ANY(metier_domaines.domaines)
                                THEN SUBSTRING(offers.code_emploi_csp FROM 3 FOR 3)
                        END AS domaine
                    FROM offers
                    JOIN metier_domaines
                        ON metier_domaines.offer_family_code = offers.code_emploi_csp
                    WHERE COALESCE(offers.functional_area_code, '') <> ''
                        AND NOT (offers.functional_area_code = ANY(metier_domaines.domaines))
                )
                UPDATE offers
                SET functional_area_code = domaines_cibles.domaine
                FROM domaines_cibles
                WHERE offers.id = domaines_cibles.id
                    AND domaines_cibles.domaine IS NOT NULL
            """,
            reverse_sql=migrations.RunSQL.noop,
            elidable=True,
        ),
    ]
