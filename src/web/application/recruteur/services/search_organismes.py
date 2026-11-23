from django.db.models import QuerySet

from application.identite.context_services.permission_service import (
    PermissionService,
)
from domain.identite.value_objects.permission_action import PermissionAction
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.django_apps.users.models import UserModel


def search_organismes(
    *, utilisateur: UserModel, nom: str, taille: int
) -> QuerySet[OrganismeModel]:
    PermissionService().can_execute(
        action=PermissionAction.LIST_ORGANISMES,
        utilisateur=utilisateur,
    )
    return (
        OrganismeModel.objects.not_supprimes().search_name(nom).stable_order()[:taille]
    )
