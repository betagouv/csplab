"""Document gateway interface for external data sources."""

from typing import List, Protocol, Tuple

from domain.entities.document import Document, DocumentType


class IDocumentGateway(Protocol):
    """Interface for fetching documents from external sources."""

    def fetch_by_type(
        self, document_type: DocumentType, start: int, batch_size: int = 1000
    ) -> Tuple[List[Document], bool]:
        """Fetch documents from external source by type."""
        ...
