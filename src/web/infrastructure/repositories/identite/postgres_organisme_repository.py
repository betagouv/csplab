from uuid import UUID

from domain.identite.entities.organisme import Organisme
from domain.identite.errors.organisme_errors import OrganismeNexistePas
from domain.identite.repositories.organisme_repository_interface import (
    IOrganismeRepository as IOrganismeIdentiteRepository,
)
from domain.identite.value_objects.siret import SIRET
from infrastructure.django_apps.recruteur.models import OrganismeModel
from infrastructure.mappers.organisme_identite_mapper import OrganismeIdentiteMapper


class PostgresOrganismeRepository(IOrganismeIdentiteRepository):
    def __init__(self) -> None:
        self._mapper_identite = OrganismeIdentiteMapper()

    def create(self, organisme: Organisme) -> Organisme:
        model = self._mapper_identite.from_domain(organisme)
        model.save()
        return organisme

    def get_by_id(self, organisme_id: UUID) -> Organisme:  # type: ignore[override]
        try:
            model = OrganismeModel.objects.get(id=organisme_id)
        except OrganismeModel.DoesNotExist as e:
            raise OrganismeNexistePas(str(organisme_id)) from e
        return self._mapper_identite.to_domain(model)

    def get_by_siret(self, siret: SIRET) -> Organisme:
        try:
            model = OrganismeModel.objects.get(siret=siret.value)
        except OrganismeModel.DoesNotExist as e:
            raise OrganismeNexistePas(siret.value) from e
        return self._mapper_identite.to_domain(model)
