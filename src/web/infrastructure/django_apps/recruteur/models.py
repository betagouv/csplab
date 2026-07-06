from django.db import models
from referentiel.value_objects.verse import Verse

from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.users.models import ProfilAgentModel
from infrastructure.django_apps.utils.models import BaseDatedModel


class OrganismeModel(BaseDatedModel):
    nom = models.CharField(max_length=255)
    versant = models.CharField(
        max_length=10,
        choices=[(v.value, v.value) for v in Verse],
    )
    siret = models.CharField(max_length=14, unique=True)
    parent_id = models.UUIDField(null=True, blank=True)
    localisation = models.JSONField(null=True, blank=True)
    etapes = models.JSONField(
        null=True,
        blank=True,
        help_text=(
            "Ordered recruitment steps. "
            "Each item: {'entity_id': str, 'categorie': str, 'nom': str}"
        ),
    )

    class Meta:
        db_table = "organisme"
        verbose_name = "Organisme"
        verbose_name_plural = "Organismes"

    def __str__(self) -> str:
        return str(self.id)


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
