from uuid import UUID

from domain.identite.entities.candidat import Candidat
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.exceptions.candidat_errors import CandidatInexistant
from domain.identite.repositories.candidat_repository_interface import (
    ICandidatRepository,
)
from infrastructure.django_apps.users.models import ProfilCandidatModel


class PostgresCandidatRepository(ICandidatRepository):
    def get_by_id(self, candidat_id: UUID) -> Candidat:
        try:
            profil = ProfilCandidatModel.objects.select_related("utilisateur").get(
                utilisateur_id=str(candidat_id)  # type: ignore[misc]  # to_field='username' (VARCHAR)
            )
            return profil.to_entity()
        except ProfilCandidatModel.DoesNotExist as e:
            raise CandidatInexistant(candidat_id) from e

    def get_by_ids(self, candidat_ids: list[UUID]) -> list[Candidat]:
        profils = ProfilCandidatModel.objects.select_related("utilisateur").filter(
            utilisateur_id__in=[str(id) for id in candidat_ids]  # type: ignore[misc]  # to_field='username' (VARCHAR)
        )
        return [profil.to_entity() for profil in profils]

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
