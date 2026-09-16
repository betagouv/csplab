from django.db import models


class MotifRefus(models.TextChoices):
    CORPS_GRADE_NON_ELIGIBLE = "corps_grade_non_eligible", "Corps ou grade non éligible"
    CONDITION_MOBILITE_NON_REMPLIE = (
        "condition_mobilite_non_remplie",
        "Condition de mobilité non remplie",
    )
    CANDIDAT_NON_FONCTIONNAIRE = (
        "candidat_non_fonctionnaire",
        "Candidat non fonctionnaire",
    )
    EXPERIENCE_INSUFFISANTE = "experience_insuffisante", "Expérience insuffisante"
    COMPETENCES_TECHNIQUES_INSUFFISANTES = (
        "competences_techniques_insuffisantes",
        "Compétences techniques insuffisantes",
    )
    NIVEAU_QUALIFICATION_INSUFFISANT = (
        "niveau_qualification_insuffisant",
        "Niveau de qualification insuffisant",
    )
    DISPONIBILITE = "disponibilite", "Disponibilité"
    AUTRE = "autre", "Autre"
