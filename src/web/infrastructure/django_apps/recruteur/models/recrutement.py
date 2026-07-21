from django.db import models

from domain.recruteur.value_objects.roles import AgentRecrutementRole
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.django_apps.referentiel.models.offer import OfferModel
from infrastructure.django_apps.users.models import (
    ProfilAgentModel,
)
from infrastructure.django_apps.utils.models import BaseDatedModel


class RecrutementModel(models.Model):
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "recrutement"
        verbose_name = "Recrutement"
        verbose_name_plural = "Recrutements"

    def __str__(self) -> str:
        return str(self.offre)


class RecrutementAgentModel(BaseDatedModel):
    recrutement = models.ForeignKey(
        RecrutementModel,
        on_delete=models.CASCADE,
        db_column="recrutement_id",
        related_name="agents_liaisons",
    )
    agent = models.ForeignKey(
        ProfilAgentModel,
        to_field="utilisateur_id",
        on_delete=models.PROTECT,
        db_column="agent_id",
        related_name="recrutements_agents",
    )
    role = models.CharField(
        max_length=20,
        choices=[(r.value, r.value) for r in AgentRecrutementRole],
        default=AgentRecrutementRole.CONTRIBUTEUR.value,
    )

    class Meta:
        db_table = "recrutement_agent"
        verbose_name = "Agent de recrutement"
        verbose_name_plural = "Agents de recrutement"
        constraints = [
            models.UniqueConstraint(
                fields=["recrutement_id", "agent_id"],
                name="unique_recrutement_agent",
            )
        ]

    def __str__(self) -> str:
        return str(self.id)
