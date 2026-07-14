from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist

from domain.recruteur.entities.recrutement import Recrutement
from domain.recruteur.errors.recrutement_errors import RecrutementInexistant
from domain.recruteur.repositories.recrutement_repository_interface import (
    IRecrutementRepository,
)
from infrastructure.django_apps.recruteur.models.recrutement import RecrutementModel
from infrastructure.mappers.recrutement_mapper import RecrutementMapper


class PostgresRecrutementRepository(IRecrutementRepository):
    def __init__(self, mapper: RecrutementMapper) -> None:
        self.mapper = mapper

    def get_by_id(self, aggregate_id: UUID) -> Recrutement:
        try:
            model = RecrutementModel.objects.get(  # type: ignore[attr-defined]
                pk=aggregate_id
            )
            return self.mapper.to_domain(model)
        except ObjectDoesNotExist as e:
            raise RecrutementInexistant(aggregate_id) from e
