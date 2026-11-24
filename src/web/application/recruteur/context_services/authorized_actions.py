from collections.abc import Collection, Sequence
from uuid import UUID

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    OperationOrganismeRefusee,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from domain.recruteur.value_objects.etape_action import EtapeAction
from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.django_apps.recruteur.models.recrutement import RecrutementModel
from infrastructure.django_apps.users.models import UserModel

organisme_permissions = OrganismePermissionService()


def authorized_actions_of_organisme(
    role: AgentOrganismeRole,
    organisme_id: UUID,
    *,
    utilisateur: UserModel,
    organisme_ids_responsable: Collection[UUID],
) -> list[str]:
    actions = {
        *organisme_permissions.authorized_actions_organisme(
            role,
            utilisateur=utilisateur,
            organisme_id=organisme_id,
            organisme_ids_responsable=organisme_ids_responsable,
        ),
        *organisme_permissions.authorized_actions_staff_organisme(utilisateur),
    }
    return [action.value for action in OrganismeAction if action in actions]


def authorized_actions_of_recrutement(
    organisme_role: AgentOrganismeRole,
    recrutement_role: str | None,
) -> list[str]:
    return [
        action.value
        for action in organisme_permissions.authorized_actions_recrutement(
            organisme_role,
            recrutement_role=(
                AgentRecrutementRole(recrutement_role) if recrutement_role else None
            ),
        )
    ]


def authorized_actions_of_etapes(
    categories: Sequence[CategorieEtapeRecrutement],
    *,
    organisme_id: UUID,
    utilisateur: UserModel,
) -> list[list[str]]:
    if not can_update_etapes(organisme_id=organisme_id, utilisateur=utilisateur):
        return [[] for _ in categories]
    en_cours = categories.count(CategorieEtapeRecrutement.EN_COURS)
    return [
        [
            action.value
            for action in categorie.actions
            if not (action == EtapeAction.DELETE_ETAPE and en_cours == 1)
        ]
        for categorie in categories
    ]


def can_update_etapes(*, organisme_id: UUID, utilisateur: UserModel) -> bool:
    try:
        organisme_permissions.can_execute(
            action=OrganismeAction.UPDATE_ORGANISME_STEPS,
            utilisateur=utilisateur,
            organisme_id=organisme_id,
        )
    except (AccesOrganismeRefuse, OperationOrganismeRefusee):
        return False
    return True


def set_recrutement_authorized_actions(recrutement: RecrutementModel) -> None:
    recrutement.authorized_actions = authorized_actions_of_recrutement(  # type: ignore[attr-defined]
        AgentOrganismeRole(recrutement.organisme_role),  # type: ignore[attr-defined]
        recrutement.recrutement_role,  # type: ignore[attr-defined]
    )


def set_etape_actions_of_organisme(
    organisme: OrganismeModel, *, utilisateur: UserModel
) -> None:
    etapes = organisme.etapes or []
    actions = authorized_actions_of_etapes(
        [CategorieEtapeRecrutement(etape["categorie"]) for etape in etapes],
        organisme_id=organisme.id,
        utilisateur=utilisateur,
    )
    organisme.etapes_with_actions = [
        {**etape, "etape_actions": etape_actions}
        for etape, etape_actions in zip(etapes, actions, strict=True)
    ]
