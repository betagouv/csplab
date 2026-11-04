from collections.abc import Iterable

from django.db.models import QuerySet

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from application.recruteur.context_services.authorized_actions import (
    authorized_actions_of_organisme,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.django_apps.users.models import UserModel


def list_organismes(*, utilisateur: UserModel) -> QuerySet[OrganismeModel]:
    OrganismePermissionService().can_execute(
        action=OrganismeAction.LIST_ORGANISMES,
        utilisateur=utilisateur,
    )
    return (
        OrganismeModel.objects.not_supprimes()
        .with_counts()
        .with_superviseurs_actifs()
        .most_recently_updated_first()
    )


def with_authorized_actions(
    organismes: Iterable[OrganismeModel], *, utilisateur: UserModel
) -> list[OrganismeModel]:
    page = list(organismes)
    for organisme in page:
        organisme.authorized_actions = authorized_actions_of_organisme(  # type: ignore[attr-defined]
            AgentOrganismeRole.SUPERVISEUR, organisme.id, utilisateur=utilisateur
        )
    return page
