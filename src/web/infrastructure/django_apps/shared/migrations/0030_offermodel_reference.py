from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shared", "0029_populate_offer_source_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="offermodel",
            name="reference",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.RunSQL(
            sql="""
                UPDATE offers
                SET reference = CASE
                    WHEN external_id LIKE '%-%'
                        THEN SUBSTRING(external_id FROM POSITION('-' IN external_id) + 1)
                    ELSE external_id
                END
            """,
            reverse_sql=migrations.RunSQL.noop,
            elidable=True,
        ),
        migrations.AlterField(
            model_name="offermodel",
            name="reference",
            field=models.CharField(max_length=100),
        ),
        migrations.AddConstraint(
            model_name="offermodel",
            constraint=models.UniqueConstraint(
                fields=["reference", "source_id"],
                name="offers_reference_source_id_unique",
            ),
        ),
    ]
