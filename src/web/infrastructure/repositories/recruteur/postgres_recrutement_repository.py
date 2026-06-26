from uuid import UUID

from ddd.page_interface import IPage

from domain.recruteur.entities.recrutement import Recrutement
from domain.recruteur.errors.erreur_recrutement import RecrutementInexistant
from domain.recruteur.repositories.recrutement_repository_interface import (
    IRecrutementRepository,
)
from domain.recruteur.value_objects.recrutement_status import RecrutementStatus
from infrastructure.django_apps.recruteur.models.recrutement import RecrutementModel
from infrastructure.mappers.queryset_page import QuerySetPageMapper
from infrastructure.mappers.recrutement_mapper import RecrutementMapper


class PostgresRecrutementRepository(IRecrutementRepository):
    def __init__(self) -> None:
        self._mapper = RecrutementMapper()

    def get_by_id(self, entity_id: UUID) -> Recrutement:
        try:
            model = RecrutementModel.objects.get(id=entity_id)  # type: ignore[attr-defined]
            return self._mapper.to_domain(model)
        except RecrutementModel.DoesNotExist as e:
            raise RecrutementInexistant(entity_id) from e

    def save(self, entity: Recrutement) -> None:
        model = self._mapper.from_domain(entity)
        model.save()

    def filter_by_status(
        self,
        organisme_id: UUID,
        status: RecrutementStatus,
    ) -> IPage[Recrutement]:
        qs = RecrutementModel.objects.filter(  # type: ignore[attr-defined]
            organisme_id=organisme_id,
            status=status.value,
        ).order_by("-updated_at")
        return QuerySetPageMapper(qs, self._mapper)
