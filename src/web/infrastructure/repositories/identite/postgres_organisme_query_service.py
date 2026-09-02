from django.db.models import Count, Max
from django.db.models.functions import Coalesce, Greatest
from referentiel.value_objects.siret import SIRET
from referentiel.value_objects.verse import Verse

from application.identite.dtos.organisme_read_models import OrganismeReadModel
from application.identite.services.organisme_query_service_interface import (
    IOrganismeQueryService,
)
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel


class PostgresOrganismeQueryService(IOrganismeQueryService):
    def get_all_with_counts(self) -> list[OrganismeReadModel]:
        models = (
            OrganismeModel.objects.annotate(
                number_agents=Count("agents_liaisons", distinct=True),
                number_published_offers=Count("recrutements", distinct=True),
                max_agent_updated=Max("agents_liaisons__updated_at"),
                last_activity_date=Greatest(
                    "updated_at",
                    Coalesce("max_agent_updated", "updated_at"),
                ),
            )
            .all()
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
                number_agents=model.number_agents,
                number_published_offers=model.number_published_offers,
            )
            for model in models
        ]
