"""Load documents strategy factory."""

from typing import Union

from application.ingestion.interfaces.load_operation_type import LoadOperationType
from domain.gateways.document_gateway_interface import IDocumentGateway
from infrastructure.exceptions.ingestion_exceptions import InvalidLoadOperationError
from infrastructure.gateways.ingestion.load_documents_strategies import (
    FetchFromApiStrategy,
    UploadFromCsvStrategy,
)


class LoadDocumentsStrategyFactory:
    """Factory for creating load documents strategies."""

    def __init__(self, document_gateway: IDocumentGateway):
        """Initialize with dependencies."""
        self.document_fetcher = document_gateway

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
