from typing import List, Protocol

from domain.entities.metier import Metier
from domain.repositories.document_repository_interface import IUpsertResult


class IMetierRepository(Protocol):
    def upsert_batch(self, metiers: List[Metier]) -> IUpsertResult: ...

    def find_by_external_id(self, external_id: str) -> Metier: ...
