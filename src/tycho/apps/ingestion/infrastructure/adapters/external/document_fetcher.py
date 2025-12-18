"""External document fetcher implementation."""

from datetime import datetime
from typing import List

from apps.ingestion.infrastructure.adapters.external.dtos.ingres_corps_dtos import (
    IngresCorpsApiResponse,
)
from apps.ingestion.infrastructure.adapters.external.dtos.talentsoft_offer_dtos import (
    TalentSoftOfferDocument,
)
from core.entities.document import Document, DocumentType
from core.repositories.document_repository_interface import IDocumentFetcher
from core.services.http_client_interface import IHttpClient
from core.services.logger_interface import ILogger


class ExternalDocumentFetcher(IDocumentFetcher):
    """Fetches documents from external API sources."""

    def __init__(
        self,
        piste_client: IHttpClient,
        talentsoft_client: IHttpClient,
        logger_service: ILogger,
    ):
        """Initialize with PISTE client, TalentSoft client, logger and source."""
        self.piste_client = piste_client
        self.talentsoft_client = talentsoft_client
        self.logger = logger_service.get_logger("ExternalDocumentFetcher")
        self._source = {
            DocumentType.CORPS: self._fetch_ingres_api,
            DocumentType.OFFER: self._fetch_talentsoft_api,
        }

    def fetch_by_type(self, document_type: DocumentType) -> List[Document]:
        """Fetch documents from external source."""
        self.logger.info(f"Fetching documents of type {document_type}")
        source = self._source.get(document_type)
        if not source:
            raise ValueError(f"No fetch source for {document_type}")
        raw_documents = source(document_type)
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
        elif document_type == DocumentType.OFFER:
            # Use Pydantic validation for TalentSoft data
            for raw_doc in raw_documents:
                offer_doc = TalentSoftOfferDocument(**raw_doc)
                # Convert string id to int for Document
                numeric_id = hash(offer_doc.id) % (10**9)
                document = Document(
                    id=numeric_id,
                    external_id=offer_doc.id,
                    raw_data=offer_doc.model_dump(),
                    type=document_type,
                    created_at=now,
                    updated_at=now,
                )
                documents.append(document)

        return documents

    def _fetch_ingres_api(self, document_type: DocumentType) -> List[dict]:
        document_type_map = {
            DocumentType.CORPS: "CORPS",
        }

        endpoint = document_type_map.get(document_type)
        if endpoint is None:
            raise ValueError(f"Ingres: unknown document type: {document_type}")

        response = self.piste_client.request(
            "GET", endpoint, params={"enVigueur": "true", "full": "true"}
        )

        raw_documents = response.json()["items"]
        self.logger.info(f"Found {len(raw_documents)} documents")
        return raw_documents

    def _fetch_talentsoft_api(self, document_type: DocumentType) -> List[dict]:
        """Fetch offers from TalentSoft API."""
        response = self.talentsoft_client.request("GET", "offers")
        raw_documents = response.json()["offers"]
        self.logger.info(f"Found {len(raw_documents)} offers")
        return raw_documents
