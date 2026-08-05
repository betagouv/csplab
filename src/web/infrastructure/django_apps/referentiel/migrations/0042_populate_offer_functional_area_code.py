from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('referentiel', '0041_offermodel_functional_area_code'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                UPDATE offers
                SET functional_area_code = LEFT(stripped.code, 3)
                FROM (
                    SELECT
                        id,
                        CASE
                            WHEN code_emploi_csp LIKE 'ER%'
                                THEN SUBSTRING(code_emploi_csp FROM 3)
                            ELSE code_emploi_csp
                        END AS code
                    FROM offers
                ) AS stripped
                WHERE offers.id = stripped.id
                    AND offers.functional_area_code IS NULL
                    AND LENGTH(stripped.code) >= 3
            """,
            reverse_sql=migrations.RunSQL.noop,
            elidable=True,
        ),
    ]
