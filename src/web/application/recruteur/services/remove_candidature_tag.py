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
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.errors.recrutement_errors import (
    RecrutementCandidatureInexistante,
)
from domain.recruteur.errors.tag_errors import TagNotOnCandidature
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.tag.models import CandidatureTagModel
from infrastructure.django_apps.users.models import UserModel
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


def remove_candidature_tag(
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    candidature_id: UUID,
    tag_id: UUID,
    utilisateur: UserModel,
) -> None:
    OrganismePermissionService().can_execute(
        action=OrganismeAction.MANAGE_TAG_ON_APPLICATION,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
    )
    contexte = RecrutementAgentService(
        organisme_id=organisme_id, recrutement_id=recrutement_id
    )
    contexte.check_recrutement_belongs_to_organisme()

    with transaction.atomic():
        if (
            CandidatureModel.objects.by_recrutement_and_candidature(
                recrutement_id, candidature_id
            )
            .select_for_update(of=("self",))
            .values_list("pk", flat=True)
            .first()
            is None
        ):
            raise RecrutementCandidatureInexistante(candidature_id)

        deleted, _ = CandidatureTagModel.objects.by_candidature_and_tag(
            candidature_id, tag_id
        ).delete()
        if deleted == 0:
            raise TagNotOnCandidature(tag_id)
        AuditLogWriter(repository=PostgresAuditLogRepository()).log_action(
            utilisateur_id=utilisateur.username,
            entity=Entity(entity_id=candidature_id),
            ressource_kind="Candidature",
            event_name="EtiquetteRetiree",
        )
