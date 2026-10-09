from collections.abc import Sequence
from uuid import UUID

from ddd.entity import Entity
from django.db import transaction

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.etapes_rules import valider_sequence_etapes
from domain.recruteur.value_objects.etape_data import EtapeData
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.django_apps.users.models import UserModel
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


def update_organisme_etapes(
    *, organisme_id: UUID, utilisateur: UserModel, etapes: Sequence[EtapeData]
) -> OrganismeModel:
    OrganismePermissionService().can_execute(
        action=OrganismeAction.UPDATE_ORGANISME_STEPS,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
    )
    valider_sequence_etapes(etapes)
    with transaction.atomic():
        try:
            organisme = (
                OrganismeModel.objects.by_id(organisme_id)
                .select_for_update(no_key=True)
                .get()
            )
        except OrganismeModel.DoesNotExist as error:
            raise OrganismeNexistePas(str(organisme_id)) from error
        changements = organisme.mettre_a_jour_etapes(etapes)
        organisme.save(update_fields=["etapes", "updated_at"])
        audit_log_writer = AuditLogWriter(repository=PostgresAuditLogRepository())
        for etape_id, event_name in changements:
            audit_log_writer.log_action(
                utilisateur_id=utilisateur.username,
                entity=Entity(entity_id=etape_id),
                ressource_kind="EtapeRecrutement",
                event_name=event_name,
            )
        audit_log_writer.log_action(
            utilisateur_id=utilisateur.username,
            entity=Entity(entity_id=organisme.id),
            ressource_kind="OrganismeRecruteur",
            event_name="OrganismeEtapesMisesAJour",
        )
    return organisme
