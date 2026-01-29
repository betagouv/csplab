"""External document fetcher implementation."""

from datetime import datetime
from typing import List, cast

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
        self.talentsoft_client = talentsoft_client
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
            # Transform Talensoft offers data
            typed_raw_documents = cast(List[dict], raw_documents)
            for idx, offer_data in enumerate(typed_raw_documents):
                offer_dict = cast(dict, offer_data)
                # Use offer ID as external_id if available, otherwise use index
                external_id = str(offer_dict.get("id", f"offer_{idx}"))
                document = Document(
                    id=0,  # Temporary ID, will be set by persister
                    external_id=external_id,
                    raw_data=offer_dict,
                    type=document_type,
                    created_at=now,
                    updated_at=now,
                )
                documents.append(document)

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

    async def _fetch_talensoft_api(
        self, document_type: DocumentType
    ) -> List[JsonDataType]:
        """Fetch offers from Talensoft API."""
        if document_type != DocumentType.OFFERS:
            raise ValueError(f"Talensoft: unsupported document type: {document_type}")

        all_offers: List[JsonDataType] = []
        start = 1
        count = 1000

        while True:
            offers_data, has_more = await self.talentsoft_client.get_offers(
                count=count, start=start
            )
            # offers_data is JsonDataType but we know it's a list from Talensoft API
            if isinstance(offers_data, list):
                all_offers.extend(offers_data)

            if not has_more:
                break

            start += count

        self.logger.info(f"Found {len(all_offers)} offers from Talensoft")
        return all_offers
