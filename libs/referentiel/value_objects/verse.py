from django.db.models import TextChoices


class Verse(TextChoices):
    FPT = "FPT", "Fonction publique Territoriale"
    FPE = "FPE", "Fonction publique de l'État"
    FPH = "FPH", "Fonction publique Hospitalière"
