from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shared", "0033_apilogmodel"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(name="ApiLogModel"),
            ],
            database_operations=[],
        ),
    ]
