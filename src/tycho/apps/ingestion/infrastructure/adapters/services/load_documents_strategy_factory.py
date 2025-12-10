"""Load documents strategy factory."""

from typing import Union

from apps.ingestion.application.interfaces.load_operation_type import LoadOperationType
from apps.ingestion.infrastructure.exceptions import InvalidLoadOperationError
from core.repositories.document_repository_interface import IDocumentFetcher

from .load_documents_strategies import FetchFromApiStrategy, UploadFromCsvStrategy


class LoadDocumentsStrategyFactory:
    """Factory for creating load documents strategies."""

    def __init__(self, document_fetcher: IDocumentFetcher):
        """Initialize with dependencies."""
        self.document_fetcher = document_fetcher

    def create(
        self, operation_type: LoadOperationType
    ) -> Union[FetchFromApiStrategy, UploadFromCsvStrategy]:
        """Create strategy based on operation type."""
        match operation_type:
            case LoadOperationType.FETCH_FROM_API:
                return FetchFromApiStrategy(self.document_fetcher)
            case LoadOperationType.UPLOAD_FROM_CSV:
                return UploadFromCsvStrategy()
            case _:
                raise InvalidLoadOperationError(str(operation_type))
