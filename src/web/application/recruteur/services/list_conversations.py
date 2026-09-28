
from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from application.recruteur.context_services.recrutement_agent_service import (
    RecrutementAgentService,
)
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.value_objects.organisme_action import OrganismeAction


def list_conversations(
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    candidature_id: UUID,
    utilisateur: Utilisateur,
) -> list[ConversationStub]:
    OrganismePermissionService().can_execute(
        action=OrganismeAction.LIST_CONVERSATIONS,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
    )
    service = RecrutementAgentService(
        organisme_id=organisme_id, recrutement_id=recrutement_id
    )
    service.check_recrutement_belongs_to_organisme()
    service.check_candidature_belongs_to_recrutement(candidature_id)

    return sorted(
        stub_conversations_of(candidature_id).values(),
        key=lambda c: c.last_message_created_at,
        reverse=True,
    )
