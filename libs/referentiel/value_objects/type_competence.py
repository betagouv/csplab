from django.db.models import TextChoices


class TypeCompetence(TextChoices):
    SAVOIR_FAIRE = "SAVOIR_FAIRE", "SAVOIR_FAIRE"
    SAVOIR_ETRE = "SAVOIR_ETRE", "SAVOIR_ETRE"
    CONNAISSANCE = "CONNAISSANCE", "CONNAISSANCE"
