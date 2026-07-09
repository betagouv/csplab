from django.db import models

from domain.candidate.value_objects.statut_candidature import StatutCandidature
from infrastructure.django_apps.recruteur.models.etape import EtapeModel
from infrastructure.django_apps.users.models import ProfilCandidatModel
from infrastructure.django_apps.utils.models import BaseDatedModel


class CandidatureModel(BaseDatedModel):
    candidat = models.ForeignKey(
        ProfilCandidatModel,
        to_field="utilisateur_id",  # UUID-as-string (VARCHAR(36))
        on_delete=models.PROTECT,
        db_column="candidat_id",
        related_name="candidatures",
    )
    statut = models.CharField(
        max_length=20,
        choices=[(s.value, s.value) for s in StatutCandidature],
        default=StatutCandidature.INITIAL.value,
    )
    documents = models.JSONField(null=True, blank=True)
    etape = models.ForeignKey(
        EtapeModel,
        on_delete=models.PROTECT,
        db_column="etape_id",
        related_name="candidatures",
        help_text=(
            "Étape courante du recrutement (par défaut, l'étape ENTREE "
            "du recrutement correspondant à l'offre)."
        ),
    )

    class Meta:
        db_table = "candidature"
        verbose_name = "Candidature"
        verbose_name_plural = "Candidatures"
        constraints = [
            models.UniqueConstraint(
                fields=["candidat_id", "etape_id"],
                name="unique_candidature_candidat_offre",
            )
        ]

    def __str__(self) -> str:
        return str(self.id)
