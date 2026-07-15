from typing import Protocol

from ddd.base_repository_interface import IBaseRepository


class ICandidatureRecruteurRepository(IBaseRepository, Protocol): ...
