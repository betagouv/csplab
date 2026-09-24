from django.db import migrations


def purge_talentsoft_organismes(apps, schema_editor):
    OfferModel = apps.get_model("referentiel", "OfferModel")
    TalentsoftOrganismeModel = apps.get_model("ingestion", "TalentsoftOrganismeModel")
    OfferModel.objects.filter(talentsoft_organisme_entity_code__isnull=False).update(
        talentsoft_organisme_entity_code=None
    )
    TalentsoftOrganismeModel.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("ingestion", "0035_alter_talentsoftorganismemodel_organisme"),
        ("referentiel", "0043_offermodel_talentsoft_organisme_entity_code"),
    ]

    operations = [
        migrations.RunPython(purge_talentsoft_organismes, migrations.RunPython.noop),
    ]
