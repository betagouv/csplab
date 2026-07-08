from django.db import models

from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.users.models import (
    ProfilAgentModel,
)
from infrastructure.django_apps.utils.models import BaseDatedModel


class NoteModel(BaseDatedModel):
    candidature = models.ForeignKey(
        CandidatureModel,
        on_delete=models.PROTECT,
        db_column="candidature_id",
        related_name="notes",
    )
    message = models.TextField()
    publie_par = models.ForeignKey(
        ProfilAgentModel,
        on_delete=models.PROTECT,
        to_field="utilisateur_id",  # UUID-as-string (VARCHAR(36))
        db_column="publie_par_id",
        related_name="notes_publiees",
    )
    supprimee_le = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "note"
        verbose_name = "Note"
        verbose_name_plural = "Notes"

    def __str__(self) -> str:
        return str(self.id)
