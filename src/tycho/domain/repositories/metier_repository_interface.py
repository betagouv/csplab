from typing import Dict, List, Protocol

from domain.entities.document import Document
from domain.entities.metier import Metier
from domain.repositories.document_repository_interface import IUpsertResult

IPredicate = Dict[str, str]


class IMetierRepository(Protocol):
    def upsert_batch(self, metiers: List[Metier]) -> IUpsertResult: ...

    def get_by_external_id(
        self, external_id_key: str, external_id_value: str
    ) -> Metier: ...

    def get_all(self) -> List[Metier]: ...

    def upsert_batch_rich_data(
        self, raw_documents: List[Document]
    ) -> IUpsertResult: ...

    def filter_by(
        self, predicate: IPredicate, limit: int = 1000
    ) -> List[
        Metier
    ]: ...  #  for example {"status": "processing"}, {"family_code": "ERLOG005"}, etc.

    def mark_as_processed(self, metiers_list: List[Metier]) -> int: ...

    def mark_as_pending(self, metiers_list: List[Metier]) -> int: ...
