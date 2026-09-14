from django.db import migrations, models


def upgrade(apps, schema_editor):
    OrganismeAgentModel = apps.get_model("recruteur", "OrganismeAgentModel")
    OrganismeAgentModel.objects.filter(role="responsable").update(role="superviseur")
    OrganismeAgentModel.objects.filter(role="membre").update(role="agent")


def downgrade(apps, schema_editor):
    OrganismeAgentModel = apps.get_model("recruteur", "OrganismeAgentModel")
    OrganismeAgentModel.objects.filter(role="superviseur").update(role="responsable")
    OrganismeAgentModel.objects.filter(role="agent").update(role="membre")


class Migration(migrations.Migration):

    dependencies = [
        ("recruteur", "0011_recrutementagentmodel_date_revocation"),
    ]

    operations = [
        migrations.RunPython(upgrade, reverse_code=downgrade),
        migrations.AlterField(
            model_name="organismeagentmodel",
            name="role",
            field=models.CharField(
                choices=[("superviseur", "superviseur"), ("agent", "agent")],
                default="agent",
                max_length=20,
            ),
        ),
    ]
