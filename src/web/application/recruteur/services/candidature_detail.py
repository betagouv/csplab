from typing import NamedTuple
from uuid import UUID

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from application.recruteur.context_services.recrutement_agent_service import (
    RecrutementAgentService,
)
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.errors.recrutement_errors import (
    RecrutementCandidatureInexistante,
)
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.candidate.models.document import DocumentModel
from infrastructure.django_apps.recruteur.models.etape import (
    EtapeModel,
    etapes_ordonnees,
)


class CandidatureDetail(NamedTuple):
    candidature: CandidatureModel
    etapes: list[EtapeModel]
    document_uuid: UUID | None
    navigation_candidature_uuids: list[UUID]


def get_candidature_detail(
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    candidature_id: UUID,
    utilisateur: Utilisateur,
) -> CandidatureDetail:
    OrganismePermissionService().can_execute(
        action=OrganismeAction.GET_CANDIDATURE_DETAIL,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
    )
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
            .get()
        )
    except CandidatureModel.DoesNotExist as error:
        raise RecrutementCandidatureInexistante(candidature_id) from error

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
    )
