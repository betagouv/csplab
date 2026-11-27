from collections.abc import Iterable
from uuid import UUID

from django.db.models import QuerySet

from application.identite.context_services.permission_service import (
    PermissionService,
)
from application.recruteur.context_services.authorized_actions import (
    authorized_actions_of_recrutement,
)
from application.recruteur.context_services.candidature_agent_service import (
    CandidatureAgentService,
)
from application.recruteur.context_services.recrutement_agent_service import (
    RecrutementAgentService,
)
from domain.identite.errors.organisme_permission_errors import OperationOrganismeRefusee
from domain.identite.value_objects.permission_action import PermissionAction
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.recruteur.models.note import NoteModel
from infrastructure.django_apps.recruteur.models.recrutement import (
    RecrutementAgentModel,
)
from infrastructure.django_apps.users.models import UserModel

_ACTIONS_SUR_SA_NOTE = frozenset(
    {PermissionAction.UPDATE_NOTE.value, PermissionAction.DELETE_NOTE.value}
)


def list_notes(
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    candidature_id: UUID,
    utilisateur: UserModel,
) -> QuerySet[NoteModel]:
    organisme_role = PermissionService().authorize(
        action=PermissionAction.LIST_NOTES,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
    )
    contexte = RecrutementAgentService(
        organisme_id=organisme_id, recrutement_id=recrutement_id
    )
    contexte.check_recrutement_belongs_to_organisme()
    candidature_service = CandidatureAgentService(
        recrutement_id=recrutement_id, candidature_id=candidature_id
    )
    candidature_service.check_candidature_belongs_to_recrutement()

    notes = (
        NoteModel.objects.by_candidature(candidature_id)
        .visibles_par(utilisateur.username)
        .with_tags()
    )
    notes.organisme_role = organisme_role  # type: ignore[attr-defined]
    return notes


def with_authorized_actions(
    notes: Iterable[NoteModel],
    *,
    organisme_role: AgentOrganismeRole | None,
    recrutement_id: UUID,
    utilisateur: UserModel,
) -> list[NoteModel]:
    page = list(notes)
    if not page:
        return page
    actions_sur_sa_note = _actions_on_own_note(
        organisme_role=organisme_role,
        recrutement_id=recrutement_id,
        utilisateur=utilisateur,
    )
    for note in page:
        note.authorized_actions = (  # type: ignore[attr-defined]
            actions_sur_sa_note if note.publie_par_id == utilisateur.username else []
        )
    return page


def _actions_on_own_note(
    *,
    organisme_role: AgentOrganismeRole | None,
    recrutement_id: UUID,
    utilisateur: UserModel,
) -> list[str]:
    # TODO : unreachable, authorize() never returns None for LIST_NOTES; kept
    # only to narrow the type for authorized_actions_of_recrutement
    if organisme_role is None:
        raise OperationOrganismeRefusee()
    recrutement_role = (
        RecrutementAgentModel.objects.by_recrutement_and_agent(
            recrutement_id, utilisateur.username
        )
        .values_list("role", flat=True)
        .first()
    )
    return [
        action
        for action in authorized_actions_of_recrutement(
            organisme_role, recrutement_role
        )
        if action in _ACTIONS_SUR_SA_NOTE
    ]
