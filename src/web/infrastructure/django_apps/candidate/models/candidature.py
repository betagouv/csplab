from uuid import UUID, uuid4

from django.db import models

from domain.candidate.entities.candidature import Candidature
from domain.candidate.value_objects.statut_candidature import StatutCandidature
from infrastructure.django_apps.utils.models import BaseDatedModel


class CandidatureModel(BaseDatedModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    candidat = models.ForeignKey(
        "users.ProfilCandidatModel",
        to_field="utilisateur_id",  # UUID-as-string (VARCHAR(36))
        on_delete=models.PROTECT,
        db_column="candidat_id",
        related_name="candidatures",
    )
    offre = models.ForeignKey(
        "referentiel.OfferModel",
        on_delete=models.PROTECT,
        db_column="offre_id",
        related_name="candidatures",
    )
    statut = models.CharField(
        max_length=20,
        choices=[(s.value, s.value) for s in StatutCandidature],
        default=StatutCandidature.INITIAL.value,
    )
    documents = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = "candidature"
        verbose_name = "Candidature"
        verbose_name_plural = "Candidatures"
        constraints = [
            models.UniqueConstraint(
                fields=["candidat_id", "offre_id"],
                name="unique_candidature_candidat_offre",
            )
        ]

    def to_entity(self) -> Candidature:
        return Candidature.build(
            entity_id=self.id,
            candidat_id=UUID(self.candidat_id),  # type: ignore[arg-type]
            offre_id=self.offre_id,  # type: ignore[attr-defined]
            statut=StatutCandidature(self.statut),
            documents=tuple(UUID(d) for d in self.documents)
            if self.documents
            else None,
            soumise_le=self.created_at,
            mise_a_jour_le=self.updated_at,
        )

    @classmethod
    def from_entity(cls, candidature: Candidature) -> "CandidatureModel":
        return cls(
            id=candidature.entity_id,
            candidat_id=str(candidature.candidat_id),  # UUID → VARCHAR(36)
            offre_id=candidature.offre_id,
            statut=candidature.statut.value,
            documents=[str(d) for d in candidature.documents]
            if candidature.documents
            else None,
        )

    def __str__(self) -> str:
        return str(self.id)
