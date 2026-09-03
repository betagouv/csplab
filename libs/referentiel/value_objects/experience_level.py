from django.db.models import TextChoices


class ExperienceLevel(TextChoices):
    DEBUTANT = "Débutant", "Débutant"
    CONFIRME = "Confirmé", "Confirmé"
    EXPERT = "Expert", "Expert"
