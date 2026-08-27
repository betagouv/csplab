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
            organisme_id=organisme_id, date_revocation__isnull=True
        ).select_related("agent__utilisateur")
        return [self._to_read_model(liaison) for liaison in liaisons]

    def get_one(
        self, *, organisme_id: UUID, agent_id: UUID
    ) -> AgentOrganismeReadModel | None:
        try:
            liaison = OrganismeAgentModel.objects.select_related(
                "agent__utilisateur"
            ).get(
                organisme_id=organisme_id,
                agent_id=agent_id,  # type: ignore[misc]
            )
        except OrganismeAgentModel.DoesNotExist:
            return None
        return self._to_read_model(liaison)

    def _to_read_model(self, liaison: OrganismeAgentModel) -> AgentOrganismeReadModel:
        return AgentOrganismeReadModel(
            entity_id=liaison.agent_id,
            organisme_id=liaison.organisme_id,
            nom=liaison.agent.utilisateur.last_name,
            prenom=liaison.agent.utilisateur.first_name,
            email=liaison.agent.utilisateur.email,
            poste=liaison.agent.intitule_poste,
            role=liaison.role,
            date_derniere_activite=liaison.agent.utilisateur.last_login,
            date_creation_compte=liaison.agent.utilisateur.date_joined,
            date_revocation=liaison.date_revocation,
        )
