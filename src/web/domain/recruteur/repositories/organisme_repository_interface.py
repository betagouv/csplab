from typing import Protocol

from ddd.base_repository_interface import IBaseRepository

from domain.recruteur.entities.organisme_recruteur import OrganismeRecruteur


class IOrganismeRecruteurRepository(IBaseRepository[OrganismeRecruteur], Protocol): ...
