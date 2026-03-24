from typing import List, Tuple

from application.ingestion.interfaces.load_operation_type import LoadOperationType
from domain.entities.document import Document, DocumentType
from domain.gateways.document_gateway_interface import IDocumentGateway
from infrastructure.exceptions.ingestion_exceptions import (
    MissingOperationParameterError,
)


class FetchFromApiStrategy:
    def __init__(self, document_gateway: IDocumentGateway):
        self.document_gateway = document_gateway

    def load_documents(self, **kwargs) -> Tuple[List[Document], bool]:
        start = kwargs.get("start", 1)

        document_type = kwargs.get("document_type")
        if not isinstance(document_type, DocumentType):
            raise MissingOperationParameterError(
                "document_type", LoadOperationType.FETCH_FROM_API.value
            )

        documents, has_more = self.document_gateway.fetch_by_type(document_type, start)
        return documents, has_more


class UploadFromCsvStrategy:
    def load_documents(self, **kwargs) -> Tuple[List[Document], bool]:
        has_more = False
        documents = kwargs.get("documents")
        if not isinstance(documents, list):
            raise MissingOperationParameterError(
                "documents", LoadOperationType.UPLOAD_FROM_CSV.value
            )

        return documents, has_more
