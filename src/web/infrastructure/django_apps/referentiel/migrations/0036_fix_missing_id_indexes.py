from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("referentiel", "0035_restore_offers_primary_key"),
    ]

    operations = [
        migrations.RunSQL(
            sql=[
                "CREATE UNIQUE INDEX IF NOT EXISTS concours_id_unique ON concours(id);",
                "CREATE UNIQUE INDEX IF NOT EXISTS corps_id_unique ON corps(id);",
                "CREATE UNIQUE INDEX IF NOT EXISTS metiers_id_unique ON metiers(id);",
            ],
        ),
    ]
