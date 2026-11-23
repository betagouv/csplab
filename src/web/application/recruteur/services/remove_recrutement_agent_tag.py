from uuid import UUID

from ddd.entity import Entity
from django.db import transaction

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from application.recruteur.context_services.recrutement_agent_service import (
    RecrutementAgentService,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.value_objects.permission_action import PermissionAction
from domain.recruteur.errors.tag_errors import TagNotOnMember
from infrastructure.django_apps.tag.models import RecrutementAgentTagModel
from infrastructure.django_apps.users.models import UserModel
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


def remove_recrutement_agent_tag(
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    agent_id: UUID,
    tag_id: UUID,
    utilisateur: UserModel,
) -> None:
    OrganismePermissionService().can_execute(
        action=PermissionAction.MANAGE_TAG_ON_MEMBER,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
    )
    contexte = RecrutementAgentService(
        organisme_id=organisme_id, recrutement_id=recrutement_id
    )
    contexte.check_recrutement_belongs_to_organisme()

    with transaction.atomic():
        membre = contexte.get_active_member(agent_id, for_update=True)
        deleted, _ = RecrutementAgentTagModel.objects.by_agent_and_tag(
            membre.pk, tag_id
        ).delete()
        if deleted == 0:
            raise TagNotOnMember(tag_id)
        AuditLogWriter(repository=PostgresAuditLogRepository()).log_action(
            utilisateur_id=utilisateur.username,
            entity=Entity(entity_id=agent_id),
            ressource_kind="RecrutementAgent",
            event_name="EtiquetteRetiree",
        )
