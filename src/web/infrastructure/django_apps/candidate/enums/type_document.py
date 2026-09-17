from django.db import models


class TypeDocument(models.TextChoices):
    CV = "cv", "CV"
    LETTRE_MOTIVATION = "lettre_motivation", "Lettre de motivation"
    PIECE_JUSTIFICATIVE = "piece_justificative", "Pièce justificative"
    AUTRE = "autre", "Autre"
