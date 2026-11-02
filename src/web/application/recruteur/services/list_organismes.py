from django.db.models import QuerySet

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.django_apps.users.models import UserModel


def list_organismes(*, utilisateur: UserModel) -> QuerySet[OrganismeModel]:
    OrganismePermissionService().can_execute(
        action=OrganismeAction.LIST_ORGANISMES,
        utilisateur=utilisateur,
    )
    return (
        OrganismeModel.objects.not_supprimes().with_counts().with_superviseurs_actifs()
    )
