from django.db import models
from referentiel.value_objects.verse import Verse

from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.referentiel.models.offer import OfferModel
from infrastructure.django_apps.users.models import (
    ProfilAgentModel,
)
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


class RecrutementModel(BaseDatedModel):
    # Override the inherited id field to use the same PK as the related OfferModel
    id = None  # type: ignore[assignment]
    offre = models.OneToOneField(
        OfferModel,
        on_delete=models.PROTECT,
        primary_key=True,
        db_column="id",
        related_name="recrutement",
    )
    organisme = models.ForeignKey(
        OrganismeModel,
        on_delete=models.PROTECT,
        db_column="organisme_id",
        related_name="recrutements",
    )
    ordre_etapes = models.JSONField(
        help_text=(
            "Liste ordonnée des UUID d'étapes (str) — ordre d'affichage "
            "Kanban uniquement. L'appartenance réelle est portée par "
            "EtapeModel.recrutement (FK), jamais par ce champ."
        ),
    )

    class Meta:
        db_table = "recrutement"
        verbose_name = "Recrutement"
        verbose_name_plural = "Recrutements"

    def __str__(self) -> str:
        return str(self.id)


class RecrutementResponsableModel(BaseDatedModel):
    recrutement = models.ForeignKey(
        RecrutementModel,
        on_delete=models.CASCADE,
        db_column="recrutement_id",
        related_name="responsables_liaisons",
    )
    agent = models.ForeignKey(
        ProfilAgentModel,
        to_field="utilisateur_id",
        on_delete=models.PROTECT,
        db_column="agent_id",
        related_name="recrutements_responsables",
    )

    class Meta:
        db_table = "recrutement_responsable"
        verbose_name = "Responsable de recrutement"
        verbose_name_plural = "Responsables de recrutement"
        constraints = [
            models.UniqueConstraint(
                fields=["recrutement_id", "agent_id"],
                name="unique_recrutement_agent",
            )
        ]

    def __str__(self) -> str:
        return str(self.id)


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
        return str(self.id)
