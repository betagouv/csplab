from django.db import models

from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from infrastructure.django_apps.recruteur.models.recrutement import RecrutementModel
from infrastructure.django_apps.utils.models import BaseDatedModel


class EtapeModel(BaseDatedModel):
    recrutement = models.ForeignKey(
        RecrutementModel,
        on_delete=models.CASCADE,
        db_column="recrutement_id",
        related_name="etapes",
    )
    categorie = models.CharField(
        max_length=20,
        choices=[(c.value, c.value) for c in CategorieEtapeRecrutement],
    )
    nom = models.CharField(max_length=255)
    ordre_candidatures = models.JSONField(
        null=True,
        blank=True,
        help_text=(
            "Liste ordonnée des UUID de candidatures (str) — ordre d'affichage "
            "au sein de cette étape uniquement. L'appartenance réelle est "
            "portée par CandidatureModel.etape (FK), jamais par ce champ."
        ),
    )

    class Meta:
        db_table = "etape_recrutement"
        verbose_name = "Étape de recrutement"
        verbose_name_plural = "Étapes de recrutement"

    def __str__(self) -> str:
        return str(self.recrutement)
