from uuid import UUID

from domain.recruteur.entities.organisme_recruteur import OrganismeRecruteur
from domain.recruteur.repositories.organisme_repository_interface import (
    IOrganismeRecruteurRepository,
)
from infrastructure.django_apps.recruteur.models import OrganismeModel
from infrastructure.mappers.organisme_recruteur_mapper import OrganismeRecruteurMapper


class PostgresOrganismeRecruteurRepository(IOrganismeRecruteurRepository):
    def __init__(self) -> None:
        self._mapper = OrganismeRecruteurMapper()

    def get_by_id(self, organisme_id: UUID) -> OrganismeRecruteur:
        model = OrganismeModel.objects.get(id=organisme_id)
        return self._mapper.to_domain(model)

    def save(self, organisme: OrganismeRecruteur) -> None:
        etapes_json = (
            self._mapper.from_domain(organisme.etapes)
            if organisme.etapes is not None
            else None
        )
        OrganismeModel.objects.filter(id=organisme.entity_id).update(etapes=etapes_json)
