import re
from datetime import datetime, timezone
from typing import Optional
from unittest.mock import patch

import pytest
from asgiref.sync import sync_to_async

from application.ingestion.interfaces.load_documents_input import LoadDocumentsInput
from application.ingestion.interfaces.load_operation_type import LoadOperationType
from application.ingestion.usecases import load_offers
from config.app_config import AppConfig
from domain.entities.document import Document, DocumentType
from domain.exceptions.document_error import InvalidDocumentTypeError
from infrastructure.di.ingestion.ingestion_container import IngestionContainer
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.django_apps.ingestion.models.raw_document import RawDocument
from infrastructure.gateways.shared.logger import LoggerService
from tests.factories.ingres_corps_factories import IngresCorpsApiResponseFactory
from tests.factories.talentsoft_factories import TalentsoftDetailOfferFactory
from tests.ingestion.unit.external_gateways.utils import (
    cached_token,
    offers_response,
)

PORT = 6333
MAX_ITERATIONS = 3


@pytest.fixture
def documents_ingestion_container():
    container = IngestionContainer()

    shared_container = SharedContainer()

    app_config = AppConfig.from_django_settings()
    shared_container.app_config.override(app_config)

    logger_service = LoggerService()
    shared_container.logger_service.override(logger_service)

    container.shared_container.override(shared_container)

    container.app_config.override(app_config)
    container.logger_service.override(logger_service)

    return container


@pytest.fixture
def test_app_config(documents_ingestion_container):
    return documents_ingestion_container.app_config()


@pytest.fixture
def load_documents_usecase(documents_ingestion_container):
    return documents_ingestion_container.load_documents_usecase()


class TestIntegrationCorpsLoadDocumentsUseCase:
    async def test_execute_returns_zero_when_no_documents(
        self, db, load_documents_usecase, test_app_config, httpx_mock
    ):
        # Mock OAuth token endpoint
        httpx_mock.add_response(
            method="POST",
            url=f"{test_app_config.piste_oauth_base_url}api/oauth/token",
            json={"access_token": "fake_token", "expires_in": 3600},
            status_code=200,
        )

        # Mock INGRES API endpoint with empty response
        httpx_mock.add_response(
            method="GET",
            url=f"{test_app_config.ingres_base_url}/CORPS",
            match_params={"enVigueur": "true", "full": "true"},
            json={"items": []},
            status_code=200,
        )

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.CORPS},
        )
        result = await load_documents_usecase.execute(input_data)
        assert result["created"] == 0
        assert result["updated"] == 0

    async def test_execute_returns_correct_count_with_documents(
        self, db, load_documents_usecase, test_app_config, httpx_mock
    ):
        api_response = IngresCorpsApiResponseFactory.build()
        api_data = [doc.model_dump(mode="json") for doc in api_response.documents]

        # Mock OAuth token endpoint
        httpx_mock.add_response(
            method="POST",
            url=f"{test_app_config.piste_oauth_base_url}api/oauth/token",
            json={"access_token": "fake_token", "expires_in": 3600},
            status_code=200,
        )

        # Mock INGRES API endpoint
        httpx_mock.add_response(
            method="GET",
            url=f"{test_app_config.ingres_base_url}/CORPS",
            match_params={"enVigueur": "true", "full": "true"},
            json={"items": api_data},
            status_code=200,
        )

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.CORPS},
        )
        result = await load_documents_usecase.execute(input_data)
        assert result["created"] == len(api_data)
        assert result["updated"] == 0

        # Verify documents are persisted in database
        @sync_to_async
        def get_saved_documents_count():
            return RawDocument.objects.filter(
                document_type=DocumentType.CORPS.value
            ).count()

        saved_count = await get_saved_documents_count()
        assert saved_count == len(api_data)


@pytest.fixture
def load_offers_usecase(documents_ingestion_container):
    return documents_ingestion_container.load_offers_usecase()


def format_modification_date(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S.") + f"{dt.microsecond // 1000:03d}"


def offersummaries_url(client, start: int) -> re.Pattern:
    return re.compile(
        rf"{re.escape(str(client.base_url))}/api/v2/offersummaries\?count=100&start={start}"
    )


def getoffer_url(client, reference: str = ".*") -> re.Pattern:
    return re.compile(
        rf"{re.escape(str(client.base_url))}/api/v2/offers/getoffer\?reference={reference}&sort=modificationDate"
    )


def mock_offersummaries_response(
    client,
    httpx_mock,
    *,
    start: int = 1,
    count_offers: int,
    has_more: bool = False,
    offers: Optional[list] = None,
):
    json = (
        offers_response(count=count_offers, has_more=has_more, offers=offers)
        if offers
        else offers_response(count=count_offers, has_more=has_more)
    )
    httpx_mock.add_response(
        method="GET", url=offersummaries_url(client, start), json=json, status_code=200
    )


def mock_detail_offer_response(client, httpx_mock, *, offer: Optional[dict] = None):
    reference = offer["reference"] if offer else None
    json = TalentsoftDetailOfferFactory.build(
        **(
            {"reference": reference, "modificationDate": offer["modificationDate"]}
            if offer
            else {}
        )
    ).model_dump()
    httpx_mock.add_response(
        method="GET",
        url=getoffer_url(client, reference or ".*"),
        json=json,
        status_code=200,
        is_reusable=offer is None,
    )


def make_document(offer: dict) -> Document:
    reference = offer["reference"]
    versant_code_obj = offer["salaryRange"]
    versant = versant_code_obj["clientCode"] if versant_code_obj else "UNK"
    return Document(
        external_id=f"{versant}-{reference}",
        raw_data=offer,
        type=DocumentType.OFFERS,
        created_at=datetime.now(timezone.utc),
    )


class TestIntegrationLoadOffersUseCase:
    async def test_raises_for_non_offers_type(self, db, load_offers_usecase):
        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.CORPS},
        )

        with pytest.raises(InvalidDocumentTypeError):
            await load_offers_usecase.execute(input_data)

    @pytest.mark.httpx_mock
    async def test_stops_when_fetch_by_type_returns_no_documents(
        self, db, httpx_mock, documents_ingestion_container, load_offers_usecase
    ):
        client = documents_ingestion_container.talentsoft_front_client()
        client.cached_token = cached_token()

        mock_offersummaries_response(client, httpx_mock, count_offers=0)

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.OFFERS},
        )

        with patch.object(
            load_offers_usecase.document_repository,
            "find_by_external_ids",
            wraps=load_offers_usecase.document_repository.find_by_external_ids,
        ) as repository_find_by_external_ids:
            result = await load_offers_usecase.execute(input_data)

        repository_find_by_external_ids.assert_not_called()
        assert result == {"created": 0, "updated": 0, "errors": []}

    async def test_stops_after_max_iterations(
        self, db, httpx_mock, documents_ingestion_container, load_offers_usecase
    ):
        client = documents_ingestion_container.talentsoft_front_client()
        client.cached_token = cached_token()

        for start in range(1, MAX_ITERATIONS):
            mock_offersummaries_response(
                client, httpx_mock, start=start, count_offers=1, has_more=True
            )
        mock_detail_offer_response(client, httpx_mock)

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.OFFERS},
        )

        with patch.object(load_offers, "MAX_ITERATIONS", MAX_ITERATIONS):
            await load_offers_usecase.execute(input_data)

        # (MAX_ITERATIONS - 1) * (getsummaries + getoffer calls)
        assert len(httpx_mock.get_requests()) == (MAX_ITERATIONS - 1) * 2
