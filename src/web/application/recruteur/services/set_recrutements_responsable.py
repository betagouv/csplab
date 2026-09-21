from typing import TypedDict
from uuid import UUID, uuid4

from ddd.entity import Entity
from django.db import transaction
from django.utils import timezone

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from application.recruteur.context_services.organisme_agent_service import (
    attach_agent_to_organisme,
    get_profil_agent,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.errors.recrutement_errors import RecrutementInexistant
from domain.recruteur.value_objects.roles import AgentRecrutementRole
from infrastructure.django_apps.recruteur.models.recrutement import (
    RecrutementAgentModel,
    RecrutementModel,
)
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


class RecrutementResponsableEchec(TypedDict):
    recrutement_id: UUID
    raison: str


class SetRecrutementsResponsableResultat(TypedDict):
    reussites: list[UUID]
    echecs: list[RecrutementResponsableEchec]


def set_recrutements_responsable(
    *,
    organisme_id: UUID,
    recrutement_ids: list[UUID],
    agent_id: UUID,
    utilisateur: Utilisateur,
) -> SetRecrutementsResponsableResultat:
    OrganismePermissionService().can_execute(
        action=OrganismeAction.SET_RECRUTEMENTS_RESPONSABLE,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
    )

    with transaction.atomic():
        agent = get_profil_agent(agent_id)
        attach_agent_to_organisme(
            organisme_id=organisme_id,
            agent=agent,
            utilisateur=utilisateur,
        )

        existing_recrutement_ids = set(
            RecrutementModel.objects.by_organisme_and_recrutements(
                organisme_id, recrutement_ids
            ).values_list("pk", flat=True)
        )

        existing_agent_roles = {
            recrutement_agent.recrutement_id: recrutement_agent
            for recrutement_agent in (
                RecrutementAgentModel.objects.get_all_by_agent_and_recrutements(
                    agent_id, existing_recrutement_ids
                )
            )
        }

        failures: list[RecrutementResponsableEchec] = [
            {"recrutement_id": rid, "raison": str(RecrutementInexistant(rid))}
            for rid in recrutement_ids
            if rid not in existing_recrutement_ids
        ]
        successes: list[UUID] = [
            rid for rid in recrutement_ids if rid in existing_recrutement_ids
        ]

        roles_to_update = list(existing_agent_roles.values())
        for recrutement_agent in roles_to_update:
            recrutement_agent.role = AgentRecrutementRole.RESPONSABLE.value
            recrutement_agent.date_revocation = None
            recrutement_agent.updated_at = timezone.now()

        roles_to_create = [
            RecrutementAgentModel(
                id=uuid4(),
                recrutement_id=recrutement_id,
                agent_id=agent_id,
                role=AgentRecrutementRole.RESPONSABLE.value,
            )
            for recrutement_id in successes
            if recrutement_id not in existing_agent_roles
        ]

        if roles_to_update:
            RecrutementAgentModel.objects.bulk_update(
                roles_to_update, ["role", "date_revocation", "updated_at"]
            )
        if roles_to_create:
            RecrutementAgentModel.objects.bulk_create(roles_to_create)

        for recrutement_id in successes:
            AuditLogWriter(repository=PostgresAuditLogRepository()).log_action(
                utilisateur_id=utilisateur.entity_id,
                entity=Entity(entity_id=recrutement_id),
                ressource_kind="RecrutementAgent",
                event_name=(
                    "AgentRecrutementModifie"
                    if recrutement_id in existing_agent_roles
                    else "AgentRecrutementAjoute"
                ),
            )

    return {"reussites": successes, "echecs": failures}
