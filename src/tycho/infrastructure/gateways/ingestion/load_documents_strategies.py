"""Load documents strategy adapters."""

from typing import List, Optional

from domain.entities.document import Document, DocumentType
from domain.repositories.document_repository_interface import IDocumentFetcher
from infrastructure.exceptions.ingestion_exceptions import (
    MissingOperationParameterError,
)


class FetchFromApiStrategy:
    """Adapter for fetching documents from external API."""

    def __init__(self, document_fetcher: IDocumentFetcher):
        """Initialize with document fetcher dependency."""
        self.document_fetcher = document_fetcher

    def load_documents(self, document_type: DocumentType) -> List[Document]:
        """Load documents from external API by document type."""
        return self.document_fetcher.fetch_by_type(document_type)


class UploadFromCsvStrategy:
    """Adapter for handling pre-validated CSV documents."""

    def __init__(self, documents: Optional[List[Document]] = None):
        """Initialize with pre-validated documents."""
        self.documents = documents or []

    def load_documents(self, document_type: DocumentType) -> List[Document]:
        """Return pre-validated documents from CSV upload."""
        if not self.documents:
            raise MissingOperationParameterError(
                "documents", f"CSV upload for {document_type.value}"
            )

        return self.documents
