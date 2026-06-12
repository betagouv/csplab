from domain.identite.entities.candidat import Candidat
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.repositories.candidat_repository_interface import (
    ICandidatRepository,
)
from infrastructure.django_apps.users.models import ProfilCandidatModel


class PostgresCandidatRepository(ICandidatRepository):
    def get_by_email(self, email: str) -> Candidat | None:
        try:
            profil = ProfilCandidatModel.objects.select_related("utilisateur").get(
                utilisateur__email=email
            )
            return profil.to_entity()
        except ProfilCandidatModel.DoesNotExist:
            return None

    def create(self, utilisateur: Utilisateur, candidat: Candidat) -> Candidat:
        ProfilCandidatModel.from_entity(utilisateur, candidat).save()
        return candidat
