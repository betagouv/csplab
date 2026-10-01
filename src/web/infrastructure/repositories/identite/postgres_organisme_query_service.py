from django.db.models import Count, Max, Prefetch, Q
from django.db.models.functions import Coalesce, Greatest
from referentiel.value_objects.siret import SIRET
from referentiel.value_objects.verse import Verse

from application.identite.dtos.organisme_read_models import (
    OrganismeReadModel,
    SuperviseurDto,
)
from application.identite.services.organisme_query_service_interface import (
    IOrganismeQueryService,
)
from infrastructure.django_apps.recruteur.models.organisme import (
    OrganismeAgentModel,
    OrganismeModel,
)


class PostgresOrganismeQueryService(IOrganismeQueryService):
    def get_all_with_counts(self) -> list[OrganismeReadModel]:
        models = (
            OrganismeModel.objects.annotate(
                number_members=Count(
                    "agents_liaisons",
                    filter=Q(agents_liaisons__date_revocation__isnull=True),
                    distinct=True,
                ),
                number_published_offers=Count("recrutements", distinct=True),
                max_agent_updated=Max("agents_liaisons__updated_at"),
                last_activity_date=Greatest(
                    "updated_at",
                    Coalesce("max_agent_updated", "updated_at"),
                ),
            )
            .prefetch_related(
                Prefetch(
                    "agents_liaisons",
                    queryset=OrganismeAgentModel.objects.superviseurs().select_related(
                        "agent__utilisateur"
                    ),
                    to_attr="superviseurs_liaisons",
                )
            )
            .order_by("-updated_at")
        )

        return [
            OrganismeReadModel(
                entity_id=model.id,
                name=model.nom,
                siret=SIRET(code=model.siret),
                verse=Verse(model.versant),
                managed_ats=model.gestion_ats or False,
                creation_date=model.created_at,
                last_activity_date=model.last_activity_date,
                superviseurs=[
                    SuperviseurDto(
                        nom=liaison.agent.utilisateur.get_full_name()
                        or liaison.agent.utilisateur.email
                    )
                    for liaison in model.superviseurs_liaisons
                ],
                number_members=model.number_members,
                number_published_offers=model.number_published_offers,
            )
            for model in models
        ]
