from typing import Protocol

from ddd.base_repository_interface import IBaseRepository

from domain.identite.entities.candidat import Candidat


class ICandidatRepository(IBaseRepository[Candidat], Protocol): ...
