from typing import Protocol

from ddd.base_repository_interface import IBaseRepository

from domain.recruteur.entities.note import Note


class INoteRepository(IBaseRepository[Note], Protocol): ...
