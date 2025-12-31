"""Load documents strategy adapters."""

from typing import List

from apps.ingestion.application.interfaces.load_operation_type import LoadOperationType
from apps.ingestion.infrastructure.exceptions import MissingOperationParameterError
from core.repositories.document_repository_interface import IDocumentFetcher
from domain.entities.document import Document, DocumentType


class FetchFromApiStrategy:
    """Adapter for fetching documents from external API."""

    def __init__(self, document_fetcher: IDocumentFetcher):
        """Initialize with document fetcher dependency."""
        self.document_fetcher = document_fetcher

    def load_documents(self, **kwargs) -> List[Document]:
        """Load documents from external API by document type."""
        document_type = kwargs.get("document_type")
        if not isinstance(document_type, DocumentType):
            raise MissingOperationParameterError(
                "document_type", LoadOperationType.FETCH_FROM_API.value
            )

        return self.document_fetcher.fetch_by_type(document_type)


class UploadFromCsvStrategy:
    """Adapter for handling pre-validated CSV documents."""

    def load_documents(self, **kwargs) -> List[Document]:
        """Return pre-validated documents from CSV upload."""
        documents = kwargs.get("documents")
        if not isinstance(documents, list):
            raise MissingOperationParameterError(
                "documents", LoadOperationType.UPLOAD_FROM_CSV.value
            )

        return documents
