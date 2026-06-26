from uuid import uuid4

from django.db import models

from domain.recruteur.value_objects.recrutement_status import RecrutementStatus
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.django_apps.users.models import ProfilCandidatModel
from infrastructure.django_apps.utils.models import BaseDatedModel


class RecrutementModel(BaseDatedModel):
    id = models.UUIDField(primary_key=True, default=uuid4)
    offre_id = models.UUIDField(db_index=True)
    organisme = models.ForeignKey(
        OrganismeModel,
        on_delete=models.PROTECT,
        related_name="recrutements",
    )
    status = models.CharField(
        max_length=20,
        choices=[(s.value, s.value) for s in RecrutementStatus],
        default=RecrutementStatus.ACTIF.value,
        db_index=True,
    )
    etapes = models.JSONField(
        default=list,
        help_text="[{'entity_id': str, 'categorie': str, 'nom': str}, ...]",
    )
    positions = models.JSONField(
        default=list,
        help_text="[{'candidature_id': str, 'etape_id': str, 'ordre': int|null}, ...]",
    )
    responsables_ids = models.JSONField(
        default=list,
        help_text="[str(uuid), ...]",
    )
    candidat_recrute = models.ForeignKey(
        ProfilCandidatModel,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        to_field="utilisateur_id",  # UUID-as-string (VARCHAR(36))
        db_column="candidat_recrute_id",
        related_name="+",
    )

    class Meta:
        db_table = "recrutement"
        verbose_name = "Recrutement"
        verbose_name_plural = "Recrutements"

    def __str__(self) -> str:
        return str(self.id)
