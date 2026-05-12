from typing import Dict, List, Protocol

from domain.entities.metier import Metier
from domain.repositories.document_repository_interface import IUpsertResult

IPredicate = Dict[str, str]


class IMetierRepository(Protocol):
    def upsert_batch(self, metiers: List[Metier]) -> IUpsertResult: ...

    def get_by_external_id(self, external_id: str) -> Metier: ...

    def get_all(self) -> List[Metier]: ...

    def filter_by(
        self, predicate: IPredicate
    ) -> List[Metier]: ...  # for example {"offer_family_code": "ERLOG005"}

    def get_pending_processing(self, limit: int = 1000) -> List[Metier]: ...

    def mark_as_processed(self, metiers_list: List[Metier]) -> int: ...

    def mark_as_pending(self, metiers_list: List[Metier]) -> int: ...
