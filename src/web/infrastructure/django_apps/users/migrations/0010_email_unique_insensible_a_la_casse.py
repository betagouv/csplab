from django.db import migrations, models
from django.db.models.functions import Lower


class Migration(migrations.Migration):
    dependencies = [
        # Doit suivre la normalisation des donnees : sur des emails encore en
        # casse mixte, la creation de l'index echouerait sur les doublons.
        ("users", "0009_emails_en_minuscules"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="usermodel",
            constraint=models.UniqueConstraint(
                Lower("email"), name="users_email_lower_unique"
            ),
        ),
    ]
