from typing import List, Protocol, Tuple

from domain.entities.document import Document, DocumentType


class IDocumentGateway(Protocol):
    async def fetch_by_type(
        self, document_type: DocumentType, start: int, batch_size: int = 1000
    ) -> Tuple[List[Document], bool]: ...

    async def get_detail(
        self, document_type: DocumentType, external_id: str
    ) -> Document: ...

    async def get_documents_to_upsert(
        self,
        document_type: DocumentType,
        fetched_documents: List[Document],
        existing_documents: List[Document],
    ) -> List[Document]: ...
