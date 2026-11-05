from ddd.mapper_interface import IToDomainMapper
from rest_framework.request import Request

from domain.identite.entities.utilisateurs import Utilisateur


class UtilisateurMapper(
    IToDomainMapper[Request, Utilisateur],
):
    def to_domain(self, request: Request) -> Utilisateur:
        user = request.user
        return Utilisateur(
            entity_id=user.username,
            email=user.email,
            prenom=user.first_name,
            nom=user.last_name,
            is_superuser=user.is_superuser,
            is_staff=user.is_staff,
        )
