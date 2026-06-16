from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("referentiel", "0034_remove_apilogmodel"),
    ]

    operations = [
        migrations.RunSQL(
            sql="CREATE UNIQUE INDEX IF NOT EXISTS offers_id_unique ON offers(id);",
        ),
    ]
