from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('referentiel', '0049_offer_champs_contrat'),
    ]

    operations = [
        migrations.RenameField(
            model_name='offermodel',
            old_name='contract_type',
            new_name='offer_nature',
        ),
    ]
