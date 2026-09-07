from typing import cast
from uuid import UUID

from ddd.entity import Entity
from django.db import models, transaction

from application.recruteur.dtos.agent_organisme_read_models import (
    AgentOrganismeReadModel,
)
from application.recruteur.services.organisme_permissions import (
    organisme_permission_service,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.errors.organisme_agent_errors import AgentNonRattache
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.recruteur.models.organisme import OrganismeAgentModel
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)
from infrastructure.repositories.recruteur.postgres_organisme_agent_query_service import (  # noqa: E501
    PostgresOrganismeAgentQueryService,
)

RESSOURCE_KIND = "AgentOrganisme"
ROLE_MODIFIE = "AgentOrganismeRoleModifie"
PROFIL_MODIFIE = "AgentOrganismeProfilModifie"


def update_organisme_agent(
    *,
    organisme_id: UUID,
    agent_id: UUID,
    utilisateur: Utilisateur,
    role: AgentOrganismeRole | None = None,
    prenom: str | None = None,
    nom: str | None = None,
    poste: str | None = None,
) -> AgentOrganismeReadModel:
    organisme_permission_service().est_autorise(
        action=OrganismeAction.UPDATE_ORGANISME_AGENT,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
    )

    with transaction.atomic():
        liaison = (
            OrganismeAgentModel.objects.select_related("agent__utilisateur")
            .filter(
                organisme_id=organisme_id,
                agent_id=agent_id,  # type: ignore[misc]
            )
            .first()
        )
        if liaison is None:
            raise AgentNonRattache(organisme_id, agent_id)

        evenements = _appliquer_modifications(
            liaison, role=role, prenom=prenom, nom=nom, poste=poste
        )

    _tracer(evenements, utilisateur_id=utilisateur.entity_id, agent_id=agent_id)

    agent_organisme = PostgresOrganismeAgentQueryService().get_one(
        organisme_id=organisme_id, agent_id=agent_id
    )
    return cast(AgentOrganismeReadModel, agent_organisme)


def _appliquer_modifications(
    liaison: OrganismeAgentModel,
    *,
    role: AgentOrganismeRole | None,
    prenom: str | None,
    nom: str | None,
    poste: str | None,
) -> list[str]:
    evenements = []

    if role is not None and liaison.role != role.value:
        liaison.role = role.value
        liaison.save(update_fields=["role", "updated_at"])
        evenements.append(ROLE_MODIFIE)

    profil = liaison.agent
    compte = profil.utilisateur

    champs_compte = _champs_modifies(compte, {"first_name": prenom, "last_name": nom})
    if champs_compte:
        compte.save(update_fields=champs_compte)

    champs_profil = _champs_modifies(profil, {"intitule_poste": poste})
    if champs_profil:
        profil.save(update_fields=[*champs_profil, "updated_at"])

    if champs_compte or champs_profil:
        evenements.append(PROFIL_MODIFIE)

    return evenements


def _champs_modifies(
    instance: models.Model, valeurs: dict[str, str | None]
) -> list[str]:
    modifies = []
    for champ, valeur in valeurs.items():
        if valeur is not None and getattr(instance, champ) != valeur:
            setattr(instance, champ, valeur)
            modifies.append(champ)
    return modifies


def _tracer(evenements: list[str], *, utilisateur_id: UUID, agent_id: UUID) -> None:
    if not evenements:
        return
    audit_log_writer = AuditLogWriter(PostgresAuditLogRepository())
    for event_name in evenements:
        audit_log_writer.log_action(
            utilisateur_id=utilisateur_id,
            entity=Entity(entity_id=agent_id),
            ressource_kind=RESSOURCE_KIND,
            event_name=event_name,
        )
