from typing import TypedDict
from uuid import UUID, uuid4

from ddd.entity import Entity
from django.db import transaction

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.errors.agent_errors import ProfilAgentNexistePas
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.errors.recrutement_errors import RecrutementInexistant
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.recruteur.models.organisme import OrganismeAgentModel
from infrastructure.django_apps.recruteur.models.recrutement import (
    RecrutementModel,
)
from infrastructure.django_apps.users.models import ProfilAgentModel
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
        if not OrganismeAgentModel.objects.by_organisme_and_agent(
            organisme_id, agent_id
        ).exists():
            if not ProfilAgentModel.objects.filter(
                utilisateur_id=agent_id  # type: ignore[misc]
            ).exists():
                raise ProfilAgentNexistePas(agent_id)

            OrganismeAgentModel.objects.update_or_create(
                organisme_id=organisme_id,
                agent_id=agent_id,  # type: ignore[misc]
                defaults={
                    "role": AgentOrganismeRole.AGENT.value,
                    "date_revocation": None,
                },
                create_defaults={
                    "id": uuid4(),
                    "role": AgentOrganismeRole.AGENT.value,
                },
            )
            AuditLogWriter(repository=PostgresAuditLogRepository()).log_action(
                utilisateur_id=utilisateur.entity_id,
                entity=Entity(entity_id=agent_id),
                ressource_kind="AgentOrganisme",
                event_name="AgentOrganismeRoleAttache",
            )

        ids = list(dict.fromkeys(recrutement_ids))
        existants = set(
            RecrutementModel.objects.by_organisme_and_recrutements(
                organisme_id, ids
            ).values_list("pk", flat=True)
        )
        echecs: list[RecrutementResponsableEchec] = [
            {"recrutement_id": rid, "raison": str(RecrutementInexistant(rid))}
            for rid in ids
            if rid not in existants
        ]

        reussites: list[UUID] = []
        for recrutement_id in ids:
            if recrutement_id not in existants:
                continue
            # TODO: placeholder for persistence and log
            reussites.append(recrutement_id)

    return {"reussites": reussites, "echecs": echecs}
