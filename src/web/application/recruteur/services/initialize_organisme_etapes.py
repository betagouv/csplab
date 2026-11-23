from uuid import UUID

from ddd.entity import Entity
from django.db import transaction

from application.identite.context_services.permission_service import (
    PermissionService,
)
from application.recruteur.context_services.authorized_actions import (
    set_etape_actions_of_organisme,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.value_objects.permission_action import PermissionAction
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.django_apps.users.models import UserModel
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


def initialize_organisme_etapes(
    *, organisme_id: UUID, utilisateur: UserModel
) -> OrganismeModel:
    PermissionService().can_execute(
        action=PermissionAction.INITIALIZE_ORGANISME_STEPS,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
    )
    with transaction.atomic():
        try:
            organisme = (
                OrganismeModel.objects.by_id(organisme_id)
                .select_for_update(no_key=True)
                .get()
            )
        except OrganismeModel.DoesNotExist as error:
            raise OrganismeNexistePas(str(organisme_id)) from error
        organisme.initialize_default_etapes()
        organisme.save(update_fields=["etapes", "updated_at"])
        AuditLogWriter(repository=PostgresAuditLogRepository()).log_action(
            utilisateur_id=utilisateur.username,
            entity=Entity(entity_id=organisme.id),
            ressource_kind="OrganismeRecruteur",
            event_name="OrganismeEtapesInitialises",
        )
    set_etape_actions_of_organisme(organisme, utilisateur=utilisateur)
    return organisme
