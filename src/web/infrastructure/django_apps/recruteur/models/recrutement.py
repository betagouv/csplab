from django.db import models

from domain.recruteur.value_objects.roles import AgentRecrutementRole
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.django_apps.referentiel.models.offer import OfferModel
from infrastructure.django_apps.users.fields import agent_fk
from infrastructure.django_apps.utils.models import BaseDatedModel


class RecrutementQuerySet(models.QuerySet):
    def by_organisme_and_recrutement(
        self, organisme_id, recrutement_id
    ) -> "RecrutementQuerySet":
        return self.filter(organisme_id=organisme_id, pk=recrutement_id)

    def by_organisme_and_recrutements(
        self, organisme_id, recrutement_ids
    ) -> "RecrutementQuerySet":
        return self.filter(organisme_id=organisme_id, pk__in=recrutement_ids)


class RecrutementModel(models.Model):
    offre = models.OneToOneField(
        OfferModel,
        on_delete=models.PROTECT,
        # to be noticed : offre is the PK
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

    objects = RecrutementQuerySet.as_manager()

    class Meta:
        db_table = "recrutement"
        verbose_name = "Recrutement"
        verbose_name_plural = "Recrutements"

    def __str__(self) -> str:
        return str(self.offre)


class RecrutementAgentQuerySet(models.QuerySet):
    def active(self) -> "RecrutementAgentQuerySet":
        return self.filter(date_revocation__isnull=True)

    def by_recrutement(self, recrutement_id) -> "RecrutementAgentQuerySet":
        return (
            self.select_related("agent__utilisateur")
            .active()
            .filter(recrutement_id=recrutement_id)
            .order_by("created_at")
        )

    def by_recrutement_and_agent(
        self, recrutement_id, agent_id
    ) -> "RecrutementAgentQuerySet":
        return self.active().filter(
            recrutement_id=recrutement_id,
            agent_id=agent_id,
        )

    def get_all_by_agent_and_recrutements(
        self, agent_id, recrutement_ids
    ) -> "RecrutementAgentQuerySet":
        return self.filter(agent_id=agent_id, recrutement_id__in=recrutement_ids)


class RecrutementAgentModel(BaseDatedModel):
    recrutement = models.ForeignKey(
        RecrutementModel,
        on_delete=models.CASCADE,
        db_column="recrutement_id",
        related_name="agents_liaisons",
    )
    agent = agent_fk(related_name="recrutements_agents")
    role = models.CharField(
        max_length=20,
        choices=[(r.value, r.value) for r in AgentRecrutementRole],
        default=AgentRecrutementRole.CONTRIBUTEUR.value,
    )
    date_revocation = models.DateTimeField(null=True, blank=True)

    objects = RecrutementAgentQuerySet.as_manager()

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
