"""External document fetcher implementation."""

from datetime import datetime
from typing import List, Tuple

from domain.entities.document import Document, DocumentType
from domain.repositories.document_repository_interface import IDocumentFetcher
from domain.services.http_client_interface import IHttpClient
from domain.services.logger_interface import ILogger
from infrastructure.external_gateways.dtos.ingres_corps_dtos import (
    IngresCorpsApiResponse,
)
from infrastructure.external_gateways.talentsoft_client import TalentsoftFrontClient


class ExternalDocumentFetcher(IDocumentFetcher):
    """Fetches documents from external API sources."""

    def __init__(
        self,
        piste_client: IHttpClient,
        talentsoft_front_client: TalentsoftFrontClient,
        logger_service: ILogger,
    ):
        """Initialize with PISTE client, logger and source."""
        self.piste_client = piste_client
        self.talentsoft_front_client = talentsoft_front_client
        self.logger = logger_service.get_logger("ExternalDocumentFetcher")
        self._source = {
            DocumentType.CORPS: self._fetch_ingres_api,
            DocumentType.GRADE: self._fetch_ingres_api,
            # TODO
            # DocumentType.CONCOURS: self._fetch_from_csv,
            # DocumentType.LAW_CONCOURS: self._fetch_legifrance_sdk,
            # DocumentType.LAW_CORPS: self._fetch_legifrance_sdk,
        }

    def fetch_by_type(
        self, document_type: DocumentType, start: int = 1
    ) -> Tuple[List[Document], bool]:
        """Fetch documents from external source."""
        self.logger.info(f"Fetching documents of type {document_type}")
        source = self._source.get(document_type)
        if not source:
            raise ValueError(f"No fetch source for {document_type}")
        raw_documents, has_more = source(document_type, start)
        now = datetime.now()
        documents = []
        if document_type == DocumentType.CORPS:
            # Use Pydantic validation for INGRES data
            validated_response = IngresCorpsApiResponse.from_list(raw_documents)
            for validated_doc in validated_response.documents:
                document = Document(
                    id=int(validated_doc.identifiant),
                    external_id=str(
                        validated_doc.identifiant
                    ),  # Use identifiant as external_id for CORPS
                    raw_data=validated_doc.model_dump(),
                    type=document_type,
                    created_at=now,  # Temporary timestamp, will be updated by persister
                    updated_at=now,  # Temporary timestamp, will be updated by persister
                )
                documents.append(document)

        return documents, has_more

    def _fetch_ingres_api(
        self, document_type: DocumentType, start: int = 1
    ) -> Tuple[List[dict], bool]:
        document_type_map = {
            DocumentType.CORPS: "CORPS",
            DocumentType.GRADE: "GRADE",
        }

        endpoint = document_type_map.get(document_type)
        if endpoint is None:
            raise ValueError(f"Ingres: unknown document type: {document_type}")

        response = self.piste_client.request(
            "GET", endpoint, params={"enVigueur": "true", "full": "true"}
        )

        raw_documents = response.json()["items"]
        self.logger.info(f"Found {len(raw_documents)} documents")

        has_more = False
        return raw_documents, has_more
