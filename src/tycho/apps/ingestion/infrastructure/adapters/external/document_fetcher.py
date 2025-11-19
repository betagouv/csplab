"""External document fetcher implementation."""

from datetime import datetime
from typing import List

from core.entities.document import Document, DocumentType
from core.interfaces.document_repository_interface import IDocumentFetcher
from core.interfaces.http_client_interface import IHttpClient
from core.interfaces.logger_interface import ILogger


class ExternalDocumentFetcher(IDocumentFetcher):
    """Fetches documents from external API sources."""

    def __init__(self, http_client: IHttpClient, logger_service: ILogger):
        """Initialize with HTTP client and logger."""
        self.http_client = http_client
        self.logger = logger_service.get_logger("ExternalDocumentFetcher")

    def fetch_by_type(self, document_type: DocumentType) -> List[Document]:
        """Fetch documents from external API by type."""
        try:
            self.logger.info(f"Fetching documents of type {document_type}")

            document_type_map = {
                DocumentType.CORPS: "CORPS",
                DocumentType.GRADE: "GRADE",
            }

            endpoint = document_type_map.get(document_type)
            if not endpoint:
                raise ValueError(f"Unknown document type: {document_type}")

            response = self.http_client.request(
                "GET", endpoint, params={"enVigueur": "true", "full": "true"}
            )

            raw_documents = response.json()["items"]
            self.logger.info(f"Found {len(raw_documents)} documents")

            # Convert to Document entities
            documents = []
            now = datetime.now()
            for raw_doc in raw_documents:
                document = Document(
                    id=raw_doc.get("identifiant"),
                    raw_data=raw_doc,
                    type=document_type,
                    created_at=now,  # Temporary timestamp, will be updated by persister
                    updated_at=now,  # Temporary timestamp, will be updated by persister
                )
                documents.append(document)

            return documents

        except Exception:
            self.logger.error("Error fetching documents")
            raise
