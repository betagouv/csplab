from typing import NamedTuple

from django.db.models import QuerySet

from infrastructure.django_apps.recruteur.models.organisme import OrganismeAgentModel
from infrastructure.django_apps.users.models import UserModel


class UtilisateurDetails(NamedTuple):
    utilisateur: UserModel
    organisme_roles: QuerySet[OrganismeAgentModel]


def get_utilisateur_details(*, utilisateur: UserModel) -> UtilisateurDetails:
    return UtilisateurDetails(
        utilisateur=utilisateur,
        organisme_roles=OrganismeAgentModel.objects.by_agent(
            utilisateur.username
        ).with_organisme(),
    )
