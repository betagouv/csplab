from typing import List
from uuid import UUID

from referentiel.entities.organisme import Organisme
from referentiel.value_objects.siret import SIRET

from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.repositories.organisme_repository_interface import (
    IOrganismeRepository as IOrganismeIdentiteRepository,
)
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.mappers.organisme_identite_mapper import OrganismeIdentiteMapper


class PostgresOrganismeRepository(IOrganismeIdentiteRepository):
    def __init__(self) -> None:
        self._mapper_identite = OrganismeIdentiteMapper()

    def create(self, organisme: Organisme) -> Organisme:
        model = self._mapper_identite.from_domain(organisme)
        model.save()
        if organisme.date_creation:
            OrganismeModel.objects.filter(pk=model.pk).update(
                created_at=organisme.date_creation
            )
        return organisme

    def get_by_id(self, organisme_id: UUID) -> Organisme:  # type: ignore[override]
        try:
            model = OrganismeModel.objects.get(id=organisme_id)
        except OrganismeModel.DoesNotExist as e:
            raise OrganismeNexistePas(str(organisme_id)) from e
        return self._mapper_identite.to_domain(model)

    def get_by_siret(self, siret: SIRET) -> Organisme | None:
        try:
            model = OrganismeModel.objects.get(siret=str(siret))
        except OrganismeModel.DoesNotExist:
            return None
        return self._mapper_identite.to_domain(model)

    def get_by_referentiel_and_external_id(
        self, referentiel: str, external_id: str
    ) -> Organisme | None:
        model = OrganismeModel.objects.filter(
            referentiel=referentiel, external_id=external_id
        ).first()
        if model is None:
            return None
        return self._mapper_identite.to_domain(model)

    def save(self, organisme: Organisme) -> None:
        try:
            model = OrganismeModel.objects.get(id=organisme.entity_id)
        except OrganismeModel.DoesNotExist as e:
            raise OrganismeNexistePas(str(organisme.entity_id)) from e
        self._mapper_identite.apply_to_model(model, organisme)
        model.save()

    def get_all(self) -> List[Organisme]:
        return [
            self._mapper_identite.to_domain(model)
            for model in OrganismeModel.objects.all()
        ]
