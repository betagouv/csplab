"""External document fetcher implementation."""

from datetime import datetime
from typing import List, cast

from asgiref.sync import async_to_sync

from domain.entities.document import Document, DocumentType
from domain.repositories.document_repository_interface import IDocumentFetcher
from domain.services.http_client_interface import IHttpClient
from domain.services.logger_interface import ILogger
from domain.types import JsonDataType
from infrastructure.external_gateways.dtos.ingres_corps_dtos import (
    IngresCorpsApiResponse,
)
from infrastructure.external_gateways.talentsoft_client import TalentsoftFrontClient


class ExternalDocumentFetcher(IDocumentFetcher):
    """Fetches documents from external API sources."""

    def __init__(
        self,
        piste_client: IHttpClient,
        talentsoft_client: TalentsoftFrontClient,
        logger_service: ILogger,
    ):
        """Initialize with PISTE client, Talensoft client, logger and source."""
        self.piste_client = piste_client
        self.talentsoft_front_client = talentsoft_client
        self.logger = logger_service.get_logger("ExternalDocumentFetcher")
        self._source = {
            DocumentType.CORPS: self._fetch_ingres_api,
            DocumentType.GRADE: self._fetch_ingres_api,
            DocumentType.OFFERS: self._fetch_talensoft_api,
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
            typed_raw_documents = cast(List[dict], raw_documents)
            validated_response = IngresCorpsApiResponse.from_list(typed_raw_documents)
            for validated_doc in validated_response.documents:
                document = Document(
                    id=int(validated_doc.identifiant),
                    external_id=str(validated_doc.identifiant),
                    raw_data=validated_doc.model_dump(),
                    type=document_type,
                    created_at=now,
                    updated_at=now,
                )
                documents.append(document)

        elif document_type == DocumentType.OFFERS:
            # For OFFERS, raw_documents is already a list of Document objects
            return cast(List[Document], raw_documents)

        return documents

    def _fetch_ingres_api(self, document_type: DocumentType) -> List[JsonDataType]:
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
        return cast(List[JsonDataType], raw_documents)

    async def _fetch_offers(self, start: int):
        """Init talentsoft_front_client with async context."""
        async with self.talentsoft_front_client:
            return await self.talentsoft_front_client.get_offers(start=start)

    def _fetch_talensoft_api(self, document_type: DocumentType) -> List[Document]:
        """Fetch offers from Talensoft API and return Document objects."""
        if document_type != DocumentType.OFFERS:
            raise ValueError(f"Talensoft: unsupported document type: {document_type}")

        # Convert async method to sync using Django's async_to_sync
        sync_fetch_offers = async_to_sync(self._fetch_offers)

        all_documents = []
        current_start = 1
        now = datetime.now()

        # Pagination loop to get all offers
        while True:
            try:
                raw_documents, has_more = sync_fetch_offers(start=current_start)
            except Exception as e:
                self.logger.error("Failed to fetch offers from Talentsoft: %s", e)
                break

            # Ensure raw_documents is a list before using len()
            if not isinstance(raw_documents, list):
                self.logger.error(
                    "Expected list of documents, got %s", type(raw_documents)
                )
                break

            if not raw_documents:
                self.logger.info("No more offers available")
                break

            self.logger.info(
                "Found %d offers from Talentsoft Front API (page starting at %d)",
                len(raw_documents),
                current_start,
            )

            # Process current batch
            for raw_doc in raw_documents:
                if not isinstance(raw_doc, dict):
                    self.logger.warning("Skipping non-dict document: %s", type(raw_doc))
                    continue

                reference = raw_doc.get("reference", None)
                if reference is None:
                    self.logger.warning(
                        "Skipping raw_doc without reference: %s", raw_doc
                    )
                    continue

                versant_dict = raw_doc.get("salaryRange", {})
                if isinstance(versant_dict, dict):
                    versant = versant_dict.get("clientCode", "UNK")
                else:
                    versant = "UNK"

                external_id = f"{versant}-{reference}"

                document = Document(
                    id=0,  # Temporary ID, will be updated by persister
                    external_id=external_id,
                    raw_data=raw_doc,
                    type=document_type,
                    created_at=now,  # Temporary timestamp, will be updated by persister
                    updated_at=now,  # Temporary timestamp, will be updated by persister
                )
                all_documents.append(document)

            # Check if we should continue
            if not has_more:
                self.logger.info("API indicates no more pages available")
                break

            current_start += 1

        self.logger.info(f"Total offers fetched: {len(all_documents)}")
        return all_documents
