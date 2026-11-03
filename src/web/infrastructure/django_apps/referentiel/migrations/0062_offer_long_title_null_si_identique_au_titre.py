from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('referentiel', '0061_offer_categories_not_empty'),
    ]

    # titre_long is now optional in the API: the ingestion only copied the title
    # into it. Clears the long titles identical to the title, so that the
    # full-text search no longer favours the offers carrying this copy, see
    # https://github.com/betagouv/csplab/issues/2202.
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
    ]
