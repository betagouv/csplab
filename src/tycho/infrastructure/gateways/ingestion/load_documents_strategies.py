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

    async def load_documents(self, **kwargs) -> Tuple[List[Document], bool]:
        start = kwargs.get("start", 1)

        documents, has_more = await self.document_gateway.fetch_by_type(
            DocumentType.CORPS, start
        )
        return documents, has_more


class UploadFromCsvStrategy:
    async def load_documents(self, **kwargs) -> Tuple[List[Document], bool]:
        has_more = False
        documents = kwargs.get("documents")
        if not isinstance(documents, list):
            raise MissingOperationParameterError(
                "documents", LoadOperationType.UPLOAD_FROM_CSV.value
            )

        return documents, has_more
