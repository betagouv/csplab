from django.db import models
from django.db.models import (
    BooleanField,
    Case,
    Count,
    F,
    Max,
    OuterRef,
    Prefetch,
    Q,
    Subquery,
    Value,
    When,
)
from django.db.models.functions import Coalesce

from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from domain.recruteur.value_objects.roles import AgentRecrutementRole
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.recruteur.models.etape import EtapeModel
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.django_apps.referentiel.models.offer import OfferModel
from infrastructure.django_apps.users.fields import agent_fk
from infrastructure.django_apps.utils.models import BaseDatedModel


class RecrutementQuerySet(models.QuerySet):
    def active_by_id(self, recrutement_id) -> "RecrutementQuerySet":
        return self.filter(pk=recrutement_id, organisme__supprime_le__isnull=True)

    def with_organisme(self) -> "RecrutementQuerySet":
        return self.select_related("organisme")

    def by_organisme(self, organisme_id) -> "RecrutementQuerySet":
        return self.filter(organisme_id=organisme_id)

    def by_organisme_and_recrutement(
        self, organisme_id, recrutement_id
    ) -> "RecrutementQuerySet":
        return self.by_organisme(organisme_id).filter(pk=recrutement_id)

    def by_organisme_and_recrutements(
        self, organisme_id, recrutement_ids
    ) -> "RecrutementQuerySet":
        return self.by_organisme(organisme_id).filter(pk__in=recrutement_ids)

    def actives(self) -> "RecrutementQuerySet":
        return self.filter(offre__archived_at__isnull=True)

    def archived(self) -> "RecrutementQuerySet":
        return self.filter(offre__archived_at__isnull=False)

    def by_agent(self, agent_id) -> "RecrutementQuerySet":
        return self.filter(
            agents_liaisons__agent_id=str(agent_id),
            agents_liaisons__date_revocation__isnull=True,
        )

    def with_offre(self) -> "RecrutementQuerySet":
        return self.select_related("offre")

    def with_detail(self) -> "RecrutementQuerySet":
        return self.with_organisme().with_offre().prefetch_related("etapes")

    def with_responsables(self) -> "RecrutementQuerySet":
        return self.prefetch_related(
            Prefetch(
                "agents_liaisons",
                queryset=RecrutementAgentModel.objects.responsables().select_related(
                    "agent__utilisateur"
                ),
                to_attr="responsables",
            )
        )

    def with_compteurs_candidatures(self) -> "RecrutementQuerySet":
        return self.annotate(
            derniere_activite=Coalesce(
                Max("etapes__candidatures__updated_at"), F("offre__publication_date")
            ),
            candidatures_total=Count("etapes__candidatures", distinct=True),
            candidatures_a_traiter=Count(
                "etapes__candidatures",
                filter=Q(etapes__categorie=CategorieEtapeRecrutement.ENTREE.value),
                distinct=True,
            ),
            candidatures_en_cours=Count(
                "etapes__candidatures",
                filter=Q(etapes__categorie=CategorieEtapeRecrutement.EN_COURS.value),
                distinct=True,
            ),
        )

    def with_recrute(self) -> "RecrutementQuerySet":
        return self.prefetch_related(
            Prefetch(
                "etapes",
                queryset=EtapeModel.objects.filter(
                    categorie=CategorieEtapeRecrutement.ACCEPTE.value
                ).prefetch_related(
                    Prefetch(
                        "candidatures",
                        queryset=CandidatureModel.objects.select_related(
                            "candidat__utilisateur"
                        ),
                    )
                ),
                to_attr="etapes_acceptees",
            )
        ).annotate(
            nb_candidatures_acceptees=Count(
                "etapes__candidatures",
                filter=Q(etapes__categorie=CategorieEtapeRecrutement.ACCEPTE.value),
                distinct=True,
            ),
            finalise=Case(
                When(nb_candidatures_acceptees__gt=0, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
        )

    def with_role_of(self, agent_id) -> "RecrutementQuerySet":
        return self.annotate(
            recrutement_role=Subquery(
                RecrutementAgentModel.objects.by_recrutement_and_agent(
                    OuterRef("pk"), agent_id
                ).values("role")[:1]
            )
        )


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

    @property
    def nom_candidat_recrute(self) -> str | None:
        etapes_acceptees = self.etapes_acceptees  # type: ignore[attr-defined]
        if not etapes_acceptees:
            return None
        candidatures = etapes_acceptees[0].candidatures.all()
        if not candidatures:
            return None
        return candidatures[0].candidat.utilisateur.get_full_name()


class RecrutementAgentQuerySet(models.QuerySet):
    def active(self) -> "RecrutementAgentQuerySet":
        return self.filter(date_revocation__isnull=True)

    def responsables(self) -> "RecrutementAgentQuerySet":
        return (
            self.active()
            .filter(role=AgentRecrutementRole.RESPONSABLE.value)
            .order_by("created_at")
        )

    def is_responsable_dans_organisme(self, agent_id, organisme_id) -> bool:
        return (
            self.responsables()
            .filter(agent_id=agent_id, recrutement__organisme_id=organisme_id)
            .exists()
        )

    def organisme_as_responsable(self, agent_id) -> "RecrutementAgentQuerySet":
        return (
            self.responsables().filter(agent_id=agent_id).select_related("recrutement")
        )

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

    @property
    def nom(self) -> str:
        return self.agent.utilisateur.get_full_name() or self.agent.utilisateur.email
