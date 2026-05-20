from typing import List

from domain.entities.source import Source
from domain.repositories.source_repository_interface import ISourceRepository


class ListSourcesUseCase:
    def __init__(self, source_repository: ISourceRepository):
        self.source_repository = source_repository

    def execute(self) -> List[Source]:
        return self.source_repository.get_all()
