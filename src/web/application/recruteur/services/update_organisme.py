from uuid import UUID

from ddd.entity import Entity
from django.db import transaction
from django.utils import timezone
from referentiel.value_objects.verse import Verse

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.value_objects.organisme_action import OrganismeAction
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.django_apps.users.models import UserModel
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


def update_organisme(
    *,
    organisme_id: UUID,
    utilisateur: UserModel,
    nom: str,
    versant: Verse,
    gestion_ats: bool,
) -> OrganismeModel:
    OrganismePermissionService().can_execute(
        action=OrganismeAction.UPDATE_ORGANISME,
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
        organisme.nom = nom
        organisme.versant = versant.value
        organisme.gestion_ats = gestion_ats
        organisme.date_derniere_activite = timezone.now()
        organisme.save(
            update_fields=[
                "nom",
                "versant",
                "gestion_ats",
                "date_derniere_activite",
                "updated_at",
            ]
        )
        AuditLogWriter(repository=PostgresAuditLogRepository()).log_action(
            utilisateur_id=utilisateur.username,
            entity=Entity(entity_id=organisme.id),
            ressource_kind="Organisme",
            event_name="OrganismeModifie",
        )
    return organisme
