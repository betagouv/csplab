from collections.abc import Sequence
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
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.django_apps.users.models import UserModel

_ACTIONS_PAR_CATEGORIE: dict[CategorieEtapeRecrutement, list[EtapeAction]] = {
    CategorieEtapeRecrutement.ENTREE: [EtapeAction.INSERT_ETAPE_AFTER],
    CategorieEtapeRecrutement.EN_COURS: list(EtapeAction),
    CategorieEtapeRecrutement.REFUS: [EtapeAction.INSERT_ETAPE_BEFORE],
    CategorieEtapeRecrutement.ACCEPTE: [],
}


def authorized_actions_of_etapes(
    categories: Sequence[CategorieEtapeRecrutement], *, can_update: bool
) -> list[list[str]]:
    if not can_update:
        return [[] for _ in categories]
    en_cours = categories.count(CategorieEtapeRecrutement.EN_COURS)
    return [
        [
            action.value
            for action in _ACTIONS_PAR_CATEGORIE[categorie]
            if not (action == EtapeAction.DELETE_ETAPE and en_cours == 1)
        ]
        for categorie in categories
    ]


def can_update_etapes(*, organisme_id: UUID, utilisateur: UserModel) -> bool:
    try:
        OrganismePermissionService().can_execute(
            action=OrganismeAction.UPDATE_ORGANISME_STEPS,
            utilisateur=utilisateur,
            organisme_id=organisme_id,
        )
    except (AccesOrganismeRefuse, OperationOrganismeRefusee):
        return False
    return True


def set_etapes_authorized_actions(
    organisme: OrganismeModel, *, utilisateur: UserModel
) -> None:
    etapes = organisme.etapes or []
    actions = authorized_actions_of_etapes(
        [CategorieEtapeRecrutement(etape["categorie"]) for etape in etapes],
        can_update=can_update_etapes(
            organisme_id=organisme.id, utilisateur=utilisateur
        ),
    )
    organisme.etapes_with_actions = [
        {**etape, "etape_actions": etape_actions}
        for etape, etape_actions in zip(etapes, actions, strict=True)
    ]
