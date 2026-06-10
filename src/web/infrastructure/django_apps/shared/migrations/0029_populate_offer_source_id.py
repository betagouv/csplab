from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ingestion", "0023_alter_source_source_id"),
        ("shared", "0028_offermodel_source_id"),
    ]

    operations = [
        migrations.RunSQL(
            sql="UPDATE offers SET source_id = (SELECT source_id FROM sources LIMIT 1)",
            reverse_sql=migrations.RunSQL.noop,
            elidable=True,
        ),
    ]
