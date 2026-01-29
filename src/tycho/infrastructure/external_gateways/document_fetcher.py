"""External document fetcher implementation."""

from datetime import datetime
from typing import List, Tuple

from asgiref.sync import async_to_sync

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
            DocumentType.OFFERS: None,
            # TODO
            # DocumentType.CONCOURS: self._fetch_from_csv,
            # DocumentType.LAW_CONCOURS: self._fetch_legifrance_sdk,
            # DocumentType.LAW_CORPS: self._fetch_legifrance_sdk,
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

        return documents

    def _fetch_ingres_api(self, document_type: DocumentType) -> List[dict]:
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
        return raw_documents

    async def _fetch_offers(self, start: int):
        """Init talentsoft_front_client with async context."""
        async with self.talentsoft_front_client:
            return await self.talentsoft_front_client.get_offers(start=start)

    def fetch_talentsoft_front_by_type(
        self, document_type: DocumentType, start: int = 1
    ) -> Tuple[List[Document], bool]:
        """Fetch documents from talensoft front external source."""
        if document_type != DocumentType.OFFERS:
            raise ValueError(
                f"Talentsoft Front API: unsupported document type: {document_type}"
            )

        # TODO remove `async_to_sync` as soon as piste_client is _asynced_ !
        # Convert async method to sync using Django's async_to_sync
        # with proper context manager
        sync_fetch_offers = async_to_sync(self._fetch_offers)

        # Run async method in sync context
        try:
            raw_documents, has_more = sync_fetch_offers(start)
        except Exception as e:
            self.logger.error("Failed to fetch offers from Talentsoft: %s", e)
            return [], False

        # Ensure raw_documents is a list before using len()
        if not isinstance(raw_documents, list):
            self.logger.error("Expected list of documents, got %s", type(raw_documents))
            return [], False

        self.logger.info(
            "Found %d offers from Talentsoft Front API", len(raw_documents)
        )

        now = datetime.now()
        documents = []

        for raw_doc in raw_documents:
            if not isinstance(raw_doc, dict):
                self.logger.warning("Skipping non-dict document: %s", type(raw_doc))
                continue

            reference = raw_doc.get("reference", None)
            if reference is None:
                self.logger.warning("Skipping raw_doc without reference: %s", raw_doc)
                continue

            versant_dict = raw_doc.get("salaryRange", {})
            versant = versant_dict.get("clientCode", "UNK")

            external_id = f"{versant}-{reference}"

            document = Document(
                id=0,  # Temporary ID, will be updated by persister
                external_id=external_id,
                raw_data=raw_doc,
                type=document_type,
                created_at=now,  # Temporary timestamp, will be updated by persister
                updated_at=now,  # Temporary timestamp, will be updated by persister
            )
            documents.append(document)

        return documents, has_more
