from typing import Dict, List
from uuid import UUID, uuid4

from domain.entities.document import Document
from domain.entities.metier import Metier
from domain.exceptions.metiers_error import MetierDoesNotExist
from domain.repositories.document_repository_interface import (
    IUpsertError,
    IUpsertResult,
)
from domain.repositories.metier_repository_interface import IMetierRepository
from domain.value_objects.verse import Verse


class InMemoryMetierRepository(IMetierRepository):
    def __init__(self) -> None:
        self._storage: Dict[UUID, Metier] = {}
        self._external_id_index: Dict[str, UUID] = {}

    def upsert_batch(self, metiers: List[Metier]) -> IUpsertResult:
        created = 0
        updated = 0
        errors: List[IUpsertError] = []

        for metier in metiers:
            try:
                if metier.id in self._storage:
                    updated += 1
                else:
                    created += 1
                self._storage[metier.id] = metier
                self._external_id_index[metier.libelle] = metier.id
            except Exception as e:
                error_detail: IUpsertError = {
                    "entity_id": metier.id,
                    "error": str(e),
                    "exception": e,
                }
                errors.append(error_detail)

        return {
            "created": created,
            "updated": updated,
            "errors": errors,
        }

    def get_by_external_id(self, external_id: str) -> Metier:
        metier_id = self._external_id_index.get(external_id)
        if metier_id is None:
            raise MetierDoesNotExist(external_id)
        return self._storage[metier_id]

    def get_all(self) -> List[Metier]:
        return list(self._storage.values())

    def upsert_batch_rich_data(self, raw_documents: List[Document]) -> IUpsertResult:
        created = 0
        updated = 0
        errors: List[IUpsertError] = []

        for doc in raw_documents:
            try:
                metier = Metier(
                    id=uuid4(),
                    libelle=doc.raw_data.get("libelle", f"Metier {doc.external_id}"),
                    description=doc.raw_data.get("description", "Description test"),
                    domaine_fonctionnel=uuid4(),
                    versants=[Verse.FPE],
                )

                if metier.id in self._storage:
                    updated += 1
                else:
                    created += 1

                self._storage[metier.id] = metier
                if doc.external_id:
                    self._external_id_index[doc.external_id] = metier.id

            except Exception as e:
                error_detail: IUpsertError = {
                    "entity_id": doc.external_id,
                    "error": str(e),
                    "exception": e,
                }
                errors.append(error_detail)

        return {
            "created": created,
            "updated": updated,
            "errors": errors,
        }

    def get_pending_processing(self, limit: int = 1000) -> List[Metier]:
        return []

    def mark_as_processed(self, metiers_list: List[Metier]) -> int:
        return 0

    def mark_as_pending(self, metiers_list: List[Metier]) -> int:
        return 0

    def clear(self) -> None:
        self._storage.clear()
        self._external_id_index.clear()
