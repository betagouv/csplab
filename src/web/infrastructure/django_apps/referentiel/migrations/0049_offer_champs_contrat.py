from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referentiel', '0048_offer_champs_export_unif'),
    ]

    operations = [
        # contract_kind passe d'une liste JSON de noms à un nom unique :
        # CDD + CDI (ou PERMANENT) -> CDD_CDI, PERMANENT -> CDI.
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql="""
                        ALTER TABLE offers
                        ALTER COLUMN contract_kind TYPE varchar(20)
                        USING CASE
                            WHEN contract_kind IS NULL
                                OR jsonb_typeof(contract_kind) <> 'array'
                                OR jsonb_array_length(contract_kind) = 0
                                THEN NULL
                            WHEN contract_kind ? 'CDD'
                                AND contract_kind ?| ARRAY['CDI', 'PERMANENT']
                                THEN 'CDD_CDI'
                            WHEN contract_kind ?| ARRAY['CDI', 'PERMANENT']
                                THEN 'CDI'
                            WHEN contract_kind ? 'CDD' THEN 'CDD'
                            WHEN contract_kind ? 'VACATION' THEN 'VACATION'
                            ELSE NULL
                        END
                    """,
                    reverse_sql="""
                        ALTER TABLE offers
                        ALTER COLUMN contract_kind TYPE jsonb
                        USING CASE
                            WHEN contract_kind IS NULL THEN NULL
                            WHEN contract_kind = 'CDD_CDI' THEN '["CDD", "CDI"]'::jsonb
                            ELSE jsonb_build_array(contract_kind)
                        END
                    """,
                ),
            ],
            state_operations=[
                migrations.AlterField(
                    model_name='offermodel',
                    name='contract_kind',
                    field=models.CharField(blank=True, max_length=20, null=True),
                ),
            ],
        ),
        migrations.RunSQL(
            sql="""
                UPDATE offers SET contract_type = 'CONTRACTUEL'
                WHERE contract_type = 'CONTRACTUELS'
            """,
            reverse_sql="""
                UPDATE offers SET contract_type = 'CONTRACTUELS'
                WHERE contract_type = 'CONTRACTUEL'
            """,
        ),
        migrations.AlterField(
            model_name='offermodel',
            name='contract_type',
            field=models.CharField(blank=True, choices=[('TITULAIRE_CONTRACTUEL', 'TITULAIRE_CONTRACTUEL'), ('CONTRACTUEL', 'CONTRACTUEL'), ('TERRITORIAL', 'TERRITORIAL')], max_length=25, null=True),
        ),
    ]
