from uuid import UUID

from domain.recruteur.entities.candidature_recruteur import CandidatureRecruteur
from domain.recruteur.errors.erreur_recrutement import CandidatureRecruteurNexistePas
from domain.recruteur.repositories.candidature_recruteur_repository_interface import (
    ICandidatureRecruteurRepository,
)
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.mappers.candidature_mappers import CandidatureRecruteurMapper


class PostgresCandidatureRecruteurRepository(ICandidatureRecruteurRepository):
    def __init__(self) -> None:
        self._mapper = CandidatureRecruteurMapper()

    def get_by_id(self, candidature_id: UUID) -> CandidatureRecruteur:
        try:
            model = CandidatureModel.objects.get(id=candidature_id)
        except CandidatureModel.DoesNotExist as e:
            raise CandidatureRecruteurNexistePas(candidature_id) from e
        return self._mapper.to_domain(model)

    def list_by_offre(self, offre_id: UUID) -> list[CandidatureRecruteur]:
        models = CandidatureModel.objects.filter(offre_id=offre_id)
        return [self._mapper.to_domain(model) for model in models]
