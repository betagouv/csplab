from uuid import UUID, uuid4

from ddd.entity import Entity
from django.db import IntegrityError, transaction
from django.utils import timezone
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.siret import SIRET
from referentiel.value_objects.verse import Verse

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.errors.organisme_errors import OrganismeSiretExisteDeja
from domain.identite.value_objects.organisme_action import OrganismeAction
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.django_apps.users.models import UserModel
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)

# Postgres' default name for the unique constraint of `organisme.siret`
SIRET_UNIQUE_CONSTRAINT = "organisme_siret_key"


def create_organisme(
    *,
    nom: str,
    versant: Verse,
    siret: str,
    utilisateur: UserModel,
    gestion_ats: bool = False,
    localisation: Localisation | None = None,
    parent_id: UUID | None = None,
) -> OrganismeModel:
    OrganismePermissionService().can_execute(
        action=OrganismeAction.CREATE_ORGANISME,
        utilisateur=utilisateur,
    )
    siret_code = SIRET(code=siret).code
    if OrganismeModel.objects.filter(siret=siret_code).exists():
        raise OrganismeSiretExisteDeja(siret_str=siret_code)

    now = timezone.now()
    with transaction.atomic():
        try:
            organisme = OrganismeModel.objects.create(
                id=uuid4(),
                nom=nom,
                versant=versant.value,
                siret=siret_code,
                gestion_ats=gestion_ats,
                parent_id=parent_id,
                localisation=_localisation_data(localisation),
                date_creation=now,
                date_derniere_activite=now,
            )
        except IntegrityError as exc:
            if SIRET_UNIQUE_CONSTRAINT in str(exc):
                raise OrganismeSiretExisteDeja(siret_str=siret_code) from exc
            raise
        AuditLogWriter(repository=PostgresAuditLogRepository()).log_action(
            utilisateur_id=utilisateur.username,
            entity=Entity(entity_id=organisme.id),
            ressource_kind="Organisme",
            event_name="OrganismeCree",
        )
    return organisme


def _localisation_data(localisation: Localisation | None) -> dict | None:
    if localisation is None:
        return None
    return {
        "area": localisation.area.value,
        "country": str(localisation.country),
        "region": localisation.region.code,
        "department": localisation.department.code,
    }
