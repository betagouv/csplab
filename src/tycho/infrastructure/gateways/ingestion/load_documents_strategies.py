"""Load documents strategy adapters."""

from typing import List, Tuple

from application.ingestion.interfaces.load_operation_type import LoadOperationType
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

    def load_documents(self, **kwargs) -> Tuple[List[Document], bool]:
        """Load documents from external API by document type."""
        start = kwargs.get("start", 1)

        document_type = kwargs.get("document_type")
        if not isinstance(document_type, DocumentType):
            raise MissingOperationParameterError(
                "document_type", LoadOperationType.FETCH_FROM_API.value
            )

        documents, has_more = self.document_fetcher.fetch_by_type(document_type, start)
        return documents, has_more


class UploadFromCsvStrategy:
    """Adapter for handling pre-validated CSV documents."""

    def load_documents(self, **kwargs) -> Tuple[List[Document], bool]:
        """Return pre-validated documents from CSV upload."""
        has_more = False
        documents = kwargs.get("documents")
        if not isinstance(documents, list):
            raise MissingOperationParameterError(
                "documents", LoadOperationType.UPLOAD_FROM_CSV.value
            )

        return documents, has_more
