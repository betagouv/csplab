from django.db import migrations


class Migration(migrations.Migration):
    replaces = [("shared", "0034_remove_apilogmodel")]

    dependencies = [
        ("referentiel", "0033_apilogmodel"),
    ]

    operations = [
        migrations.DeleteModel(name="ApiLogModel"),
    ]
