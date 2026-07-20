from django.db import models
from referentiel.value_objects.verse import Verse

from domain.recruteur.value_objects.roles import AgentOrganismeRole
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


class OrganismeAgentModel(BaseDatedModel):
    organisme = models.ForeignKey(
        OrganismeModel,
        on_delete=models.CASCADE,
        db_column="organisme_id",
        related_name="agents_liaisons",
    )
    agent = models.ForeignKey(
        ProfilAgentModel,
        to_field="utilisateur_id",
        on_delete=models.PROTECT,
        db_column="agent_id",
        related_name="organismes_agents",
    )
    role = models.CharField(
        max_length=20,
        choices=[(r.value, r.value) for r in AgentOrganismeRole],
        default=AgentOrganismeRole.MEMBRE.value,
    )

    class Meta:
        db_table = "organisme_agent"
        verbose_name = "Agent d'organisme"
        verbose_name_plural = "Agents d'organisme"
        constraints = [
            models.UniqueConstraint(
                fields=["organisme_id", "agent_id"],
                name="unique_organisme_agent",
            )
        ]

    def __str__(self) -> str:
        return str(self.id)
