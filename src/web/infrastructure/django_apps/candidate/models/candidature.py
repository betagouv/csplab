from uuid import UUID, uuid4

from django.db import models

from domain.candidate.entities.candidature import Candidature
from domain.candidate.value_objects.statut_candidature import StatutCandidature


class CandidatureModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    candidat_id = models.UUIDField()
    offre_id = models.UUIDField()
    statut = models.CharField(
        max_length=20,
        choices=[(s.value, s.value) for s in StatutCandidature],
        default=StatutCandidature.INITIAL.value,
    )
    documents = models.JSONField(null=True, blank=True)
    soumise_le = models.DateTimeField(null=True, blank=True)
    mise_a_jour_le = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "candidature"
        verbose_name = "Candidature"
        verbose_name_plural = "Candidatures"
        unique_together = [("candidat_id", "offre_id")]

    def to_entity(self) -> Candidature:
        return Candidature.build(
            entity_id=self.id,
            candidat_id=self.candidat_id,
            offre_id=self.offre_id,
            statut=StatutCandidature(self.statut),
            documents=tuple(UUID(d) for d in self.documents)
            if self.documents
            else None,
            soumise_le=self.soumise_le,
            mise_a_jour_le=self.mise_a_jour_le,
        )

    @classmethod
    def from_entity(cls, candidature: Candidature) -> "CandidatureModel":
        return cls(
            id=candidature.entity_id,
            candidat_id=candidature.candidat_id,
            offre_id=candidature.offre_id,
            statut=candidature.statut.value,
            documents=[str(d) for d in candidature.documents]
            if candidature.documents
            else None,
            soumise_le=candidature.soumise_le,
            mise_a_jour_le=candidature.mise_a_jour_le,
        )

    def __str__(self) -> str:
        return str(self.id)
