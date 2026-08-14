from typing import Protocol

from ddd.base_repository_interface import IBaseRepository

from domain.recruteur.entities.recrutement import Recrutement


class IRecrutementRepository(IBaseRepository[Recrutement], Protocol): ...
