from typing import NamedTuple
from uuid import UUID

from application.identite.context_services.permission_service import (
    PermissionService,
)
from application.recruteur.context_services.authorized_actions import (
    authorized_actions_of_recrutement,
)
from application.recruteur.context_services.recrutement_agent_service import (
    RecrutementAgentService,
)
from domain.identite.errors.organisme_permission_errors import OperationOrganismeRefusee
from domain.identite.value_objects.permission_action import PermissionAction
from domain.recruteur.errors.recrutement_errors import (
    RecrutementCandidatureInexistante,
)
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.candidate.models.document import DocumentModel
from infrastructure.django_apps.recruteur.models.etape import (
    EtapeModel,
    etapes_ordonnees,
)
from infrastructure.django_apps.recruteur.models.recrutement import (
    RecrutementAgentModel,
)
from infrastructure.django_apps.users.models import UserModel


class CandidatureDetail(NamedTuple):
    candidature: CandidatureModel
    etapes: list[EtapeModel]
    document_uuid: UUID | None
    navigation_candidature_uuids: list[UUID]
    authorized_actions: list[str]


def get_candidature(
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    candidature_id: UUID,
    utilisateur: UserModel,
) -> CandidatureDetail:
    organisme_role = PermissionService().authorize(
        action=PermissionAction.GET_CANDIDATURE,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
    )
    if organisme_role is None:
        raise OperationOrganismeRefusee()
    contexte = RecrutementAgentService(
        organisme_id=organisme_id, recrutement_id=recrutement_id
    )
    contexte.check_recrutement_belongs_to_organisme()

    try:
        candidature = (
            CandidatureModel.objects.by_recrutement_and_candidature(
                recrutement_id, candidature_id
            )
            .with_detail()
            .with_tags()
            .get()
        )
    except CandidatureModel.DoesNotExist as error:
        raise RecrutementCandidatureInexistante(candidature_id) from error

    recrutement_role = (
        RecrutementAgentModel.objects.by_recrutement_and_agent(
            recrutement_id, utilisateur.username
        )
        .values_list("role", flat=True)
        .first()
    )

    return CandidatureDetail(
        candidature=candidature,
        etapes=etapes_ordonnees(candidature.etape.recrutement),
        document_uuid=DocumentModel.objects.cvs_of(candidature.id)
        .values_list("id", flat=True)
        .first(),
        navigation_candidature_uuids=list(
            CandidatureModel.objects.by_etape(candidature.etape_id).values_list(
                "id", flat=True
            )
        ),
        authorized_actions=authorized_actions_of_recrutement(
            organisme_role, recrutement_role
        ),
    )
