from collections.abc import Sequence
from uuid import UUID, uuid4

from django.db import models
from django.db.models import Q
from referentiel.value_objects.verse import Verse

from domain.recruteur.errors.organisme_recruteur_errors import (
    ConfigurationEtapesInvalide,
)
from domain.recruteur.value_objects.etape_data import EtapeData
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.recruteur.enums.etape_par_defaut import EtapeParDefaut
from infrastructure.django_apps.users.fields import agent_fk
from infrastructure.django_apps.utils.models import BaseDatedModel


class OrganismeQuerySet(models.QuerySet):
    def not_supprimes(self) -> "OrganismeQuerySet":
        return self.filter(supprime_le__isnull=True)

    def by_id(self, organisme_id) -> "OrganismeQuerySet":
        return self.not_supprimes().filter(pk=organisme_id)

    def by_organisme_ids(self, organisme_ids) -> "OrganismeQuerySet":
        return self.filter(pk__in=organisme_ids)

    def etapes_of(self, organisme_id) -> "OrganismeQuerySet":
        return self.filter(pk=organisme_id).only("id", "etapes")

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

    def initialize_default_etapes(self) -> None:
        self.etapes = [
            {
                "entity_id": str(uuid4()),
                "categorie": etape.categorie.value,
                "nom": etape.nom,
            }
            for etape in EtapeParDefaut
        ]

    def mettre_a_jour_etapes(
        self, etapes: Sequence[EtapeData]
    ) -> list[tuple[UUID, str]]:
        anciennes = {
            UUID(etape["entity_id"]): (rang, etape)
            for rang, etape in enumerate(self.etapes or [])
        }
        nouvelles = []
        changements = []
        for rang, etape in enumerate(etapes):
            if etape.etape_uuid is None:
                etape_id = uuid4()
                changements.append((etape_id, "EtapeAjoutee"))
            else:
                etape_id = etape.etape_uuid
                if etape_id not in anciennes:
                    raise ConfigurationEtapesInvalide(f"Étape inconnue : {etape_id}")
                ancien_rang, ancienne = anciennes[etape_id]
                if ancienne["categorie"] != etape.categorie.value:
                    raise ConfigurationEtapesInvalide(
                        "La catégorie d'une étape existante ne peut pas changer"
                    )
                if ancienne["nom"] != etape.nom:
                    changements.append((etape_id, "EtapeRenommee"))
                if ancien_rang != rang:
                    changements.append((etape_id, "EtapeReordonnee"))
            nouvelles.append(
                {
                    "entity_id": str(etape_id),
                    "categorie": etape.categorie.value,
                    "nom": etape.nom,
                }
            )
        conservees = {etape.etape_uuid for etape in etapes}
        changements += [
            (etape_id, "EtapeSupprimee")
            for etape_id in anciennes
            if etape_id not in conservees
        ]
        self.etapes = nouvelles
        return changements


class OrganismeAgentQuerySet(models.QuerySet):
    def active(self) -> "OrganismeAgentQuerySet":
        return self.filter(date_revocation__isnull=True)

    def by_agent(self, agent_id) -> "OrganismeAgentQuerySet":
        return self.active().filter(agent_id=agent_id)

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
