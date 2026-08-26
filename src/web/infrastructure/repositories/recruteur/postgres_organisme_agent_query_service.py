from uuid import UUID

from application.recruteur.dtos.agent_organisme_read_models import (
    AgentOrganismeReadModel,
)
from application.recruteur.services.organisme_agent_query_service_interface import (
    IOrganismeAgentQueryService,
)
from infrastructure.django_apps.recruteur.models.organisme import OrganismeAgentModel


class PostgresOrganismeAgentQueryService(IOrganismeAgentQueryService):
    def list_by_organisme(self, *, organisme_id: UUID) -> list[AgentOrganismeReadModel]:
        liaisons = OrganismeAgentModel.objects.filter(
            organisme_id=organisme_id
        ).select_related("agent__utilisateur")
        return [
            AgentOrganismeReadModel(
                entity_id=liaison.agent_id,
                organisme_id=liaison.organisme_id,
                nom=liaison.agent.utilisateur.last_name,
                prenom=liaison.agent.utilisateur.first_name,
                email=liaison.agent.utilisateur.email,
                poste=liaison.agent.intitule_poste,
                role=liaison.role,
            )
            for liaison in liaisons
        ]
