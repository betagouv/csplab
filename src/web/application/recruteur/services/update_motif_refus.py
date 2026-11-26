from datetime import datetime, timezone
from uuid import UUID

from ddd.entity import Entity
from django.db import transaction

from application.identite.context_services.permission_service import (
    PermissionService,
)
from application.recruteur.context_services.recrutement_agent_service import (
    RecrutementAgentService,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.value_objects.permission_action import PermissionAction
from domain.recruteur.errors.recrutement_errors import (
    CandidatureNonRefusee,
    RecrutementCandidatureInexistante,
)
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.users.models import UserModel
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


def update_motif_refus(
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    candidature_id: UUID,
    motif_refus: str,
    utilisateur: UserModel,
) -> CandidatureModel:
    PermissionService().authorize(
        action=PermissionAction.UPDATE_MOTIF_REFUS,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
    )
    RecrutementAgentService(
        organisme_id=organisme_id, recrutement_id=recrutement_id
    ).check_recrutement_belongs_to_organisme()

    with transaction.atomic():
        try:
            candidature = CandidatureModel.objects.for_motif_refus_update(
                recrutement_id, candidature_id
            ).get()
        except CandidatureModel.DoesNotExist as error:
            raise RecrutementCandidatureInexistante(candidature_id) from error

        if not candidature.etape.motif_refus_required:
            raise CandidatureNonRefusee(candidature_id)
        if candidature.motif_refus == motif_refus:
            return candidature

        candidature.motif_refus = motif_refus
        candidature.updated_by_recruteur = datetime.now(tz=timezone.utc)
        candidature.save(
            update_fields=["motif_refus", "updated_by_recruteur", "updated_at"]
        )
        AuditLogWriter(repository=PostgresAuditLogRepository()).log_action(
            utilisateur_id=utilisateur.username,
            entity=Entity(entity_id=candidature.id),
            ressource_kind="CandidatureRecruteur",
            event_name="MotifRefusModifie",
        )
    return candidature
