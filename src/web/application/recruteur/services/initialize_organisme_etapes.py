from uuid import UUID

from ddd.entity import Entity
from django.db import transaction

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.value_objects.organisme_action import OrganismeAction
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.django_apps.users.models import UserModel
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


def initialize_organisme_etapes(
    *, organisme_id: UUID, utilisateur: UserModel
) -> OrganismeModel:
    # can_execute lève OrganismeNexistePas si l'organisme n'existe pas
    OrganismePermissionService().can_execute(
        action=OrganismeAction.INITIALIZE_ORGANISME_STEPS,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
    )
    with transaction.atomic():
        # Verrou pour que lecture et écriture restent cohérentes dans la transaction
        # (#1686 lira avant d'écrire) ; NO KEY pour ne pas bloquer les insertions
        # des tables liées
        organisme = OrganismeModel.objects.select_for_update(no_key=True).get(
            id=organisme_id
        )
        organisme.initialize_default_etapes()
        organisme.save(update_fields=["etapes", "updated_at"])
        AuditLogWriter(repository=PostgresAuditLogRepository()).log_action(
            utilisateur_id=utilisateur.username,
            entity=Entity(entity_id=organisme.id),
            ressource_kind="OrganismeRecruteur",
            event_name="OrganismeEtapesInitialises",
        )
    return organisme
