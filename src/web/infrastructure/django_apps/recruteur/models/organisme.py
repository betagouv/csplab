from django.db import models
from django.db.models import Q
from referentiel.value_objects.verse import Verse

from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.users.fields import agent_fk
from infrastructure.django_apps.utils.models import BaseDatedModel


class OrganismeQuerySet(models.QuerySet):
    def not_supprimes(self) -> "OrganismeQuerySet":
        return self.filter(supprime_le__isnull=True)

    def by_organisme_ids(self, organisme_ids) -> "OrganismeQuerySet":
        return self.filter(pk__in=organisme_ids)

    def by_referentiel_and_external_id_pairs(
        self, pairs: list[tuple[str, str]]
    ) -> "OrganismeQuerySet":
        if not pairs:
            return self.none()
        query = Q()
        for referentiel, external_id in pairs:
            query |= Q(referentiel=referentiel, external_id=external_id)
        return self.filter(query)


class OrganismeModel(BaseDatedModel):
    nom = models.CharField(max_length=255)
    versant = models.CharField(
        max_length=10,
        choices=[(v.value, v.value) for v in Verse],
    )
    siret = models.CharField(max_length=14, unique=True)
    external_id = models.CharField(max_length=50, null=True, blank=True)
    referentiel = models.CharField(max_length=50, null=True, blank=True)
    millesime = models.CharField(max_length=25, null=True, blank=True)
    gestion_ats = models.BooleanField(null=True, blank=True, default=False)
    date_creation = models.DateTimeField(null=True, blank=True)
    date_derniere_activite = models.DateTimeField(null=True, blank=True)
    parent_id = models.UUIDField(null=True, blank=True)
    localisation = models.JSONField(null=True, blank=True)
    supprime_le = models.DateTimeField(null=True, blank=True, db_index=True)
    etapes = models.JSONField(
        null=True,
        blank=True,
        help_text=(
            "Ordered recruitment steps. "
            "Each item: {'entity_id': str, 'categorie': str, 'nom': str}"
        ),
    )

    objects = OrganismeQuerySet.as_manager()

    class Meta:
        db_table = "organisme"
        verbose_name = "Organisme"
        verbose_name_plural = "Organismes"

    def __str__(self) -> str:
        return str(self.id)


class OrganismeAgentQuerySet(models.QuerySet):
    def active(self) -> "OrganismeAgentQuerySet":
        return self.filter(date_revocation__isnull=True)

    def by_organisme_and_agent(
        self, organisme_id, agent_id
    ) -> "OrganismeAgentQuerySet":
        return self.active().filter(
            organisme_id=organisme_id,
            agent_id=agent_id,
        )


class OrganismeAgentModel(BaseDatedModel):
    organisme = models.ForeignKey(
        OrganismeModel,
        on_delete=models.CASCADE,
        db_column="organisme_id",
        related_name="agents_liaisons",
    )
    agent = agent_fk(related_name="organismes_agents")
    role = models.CharField(
        max_length=20,
        choices=[(r.value, r.value) for r in AgentOrganismeRole],
        default=AgentOrganismeRole.AGENT.value,
    )
    date_revocation = models.DateTimeField(null=True, blank=True)

    objects = OrganismeAgentQuerySet.as_manager()

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
