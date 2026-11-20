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
from infrastructure.django_apps.recruteur.models.etape import EtapeModel
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.django_apps.users.models import UserModel

_ACTIONS_PAR_CATEGORIE: dict[CategorieEtapeRecrutement, list[EtapeAction]] = {
    CategorieEtapeRecrutement.ENTREE: [EtapeAction.INSERT_ETAPE_AFTER],
    CategorieEtapeRecrutement.EN_COURS: list(EtapeAction),
    CategorieEtapeRecrutement.REFUS: [EtapeAction.INSERT_ETAPE_BEFORE],
    CategorieEtapeRecrutement.ACCEPTE: [],
}


def authorized_actions_of_etapes(
    categories: Sequence[CategorieEtapeRecrutement],
    *,
    can_update: bool,
    nb_candidatures: Sequence[int] | None = None,
) -> list[list[str]]:
    if not can_update:
        return [[] for _ in categories]
    en_cours = categories.count(CategorieEtapeRecrutement.EN_COURS)
    nb_candidatures = nb_candidatures or [0] * len(categories)
    return [
        [
            action.value
            for action in _ACTIONS_PAR_CATEGORIE[categorie]
            if not (
                action == EtapeAction.DELETE_ETAPE and (en_cours == 1 or nb_candidats)
            )
        ]
        for categorie, nb_candidats in zip(categories, nb_candidatures, strict=True)
    ]


def can_update_etapes(*, organisme_id: UUID, utilisateur: UserModel) -> bool:
    return _is_allowed(
        action=OrganismeAction.UPDATE_ORGANISME_STEPS,
        organisme_id=organisme_id,
        utilisateur=utilisateur,
    )


def can_update_recrutement_etapes(
    *, organisme_id: UUID, recrutement_id: UUID, utilisateur: UserModel
) -> bool:
    return _is_allowed(
        action=OrganismeAction.UPDATE_RECRUTEMENT_ETAPES,
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
        utilisateur=utilisateur,
    )


def _is_allowed(
    *,
    action: OrganismeAction,
    organisme_id: UUID,
    utilisateur: UserModel,
    recrutement_id: UUID | None = None,
) -> bool:
    try:
        OrganismePermissionService().can_execute(
            action=action,
            utilisateur=utilisateur,
            organisme_id=organisme_id,
            recrutement_id=recrutement_id,
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


def set_recrutement_etapes_authorized_actions(
    etapes: Sequence[EtapeModel],
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    utilisateur: UserModel,
) -> None:
    nb_candidatures = dict(
        EtapeModel.objects.filter(pk__in=[etape.pk for etape in etapes])
        .with_nb_candidatures()
        .values_list("pk", "nb_candidatures")
    )
    actions = authorized_actions_of_etapes(
        [CategorieEtapeRecrutement(etape.categorie) for etape in etapes],
        can_update=can_update_recrutement_etapes(
            organisme_id=organisme_id,
            recrutement_id=recrutement_id,
            utilisateur=utilisateur,
        ),
        nb_candidatures=[nb_candidatures[etape.pk] for etape in etapes],
    )
    for etape, etape_actions in zip(etapes, actions, strict=True):
        etape.etape_actions = etape_actions  # type: ignore[attr-defined]
