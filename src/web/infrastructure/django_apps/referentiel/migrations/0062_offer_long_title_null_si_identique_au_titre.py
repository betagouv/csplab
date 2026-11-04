from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referentiel', '0061_offer_categories_not_empty'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                UPDATE offers
                SET long_title = NULL
                WHERE long_title = title
            """,
            reverse_sql=migrations.RunSQL.noop,
            elidable=True,
        ),
        migrations.AddConstraint(
            model_name='offermodel',
            constraint=models.CheckConstraint(condition=models.Q(('long_title', models.F('title')), _negated=True), name='offer_long_title_differs_from_title'),
        ),
    ]
