from django.db import migrations, models
from django.db.models import Q
from django.db.models.functions import Lower, Trim


def lowercase_emails(apps, schema_editor):
    UserModel = apps.get_model("users", "UserModel")
    UserModel.objects.update(email=Trim(Lower("email")))


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0008_alter_usermodel_username"),
    ]

    operations = [
        migrations.RunPython(
            lowercase_emails, migrations.RunPython.noop, elidable=True
        ),
        migrations.AddConstraint(
            model_name="usermodel",
            constraint=models.CheckConstraint(
                condition=Q(email=Trim(Lower("email"))),
                name="users_email_is_lowercase",
            ),
        ),
    ]
