import re
from datetime import datetime, timezone
from typing import Optional
from unittest.mock import patch

import pytest

from application.ingestion.interfaces.load_documents_input import LoadDocumentsInput
from application.ingestion.interfaces.load_operation_type import LoadOperationType
from application.ingestion.usecases import load_offers
from domain.entities.document import Document, DocumentType
from domain.exceptions.document_error import InvalidDocumentTypeError
from tests.factories.talentsoft_factories import TalentsoftDetailOfferFactory
from tests.ingestion.unit.external_gateways.utils import (
    cached_token,
    offers_response,
)

PORT = 6333
MAX_ITERATIONS = 3


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


@pytest.mark.httpx_mock(should_mock=lambda request: request.url.port != PORT)
class TestIntegrationLoadOffersUseCase:
    async def test_raises_for_non_offers_type(
        self, db, httpx_mock, ingestion_integration_container
    ):
        usecase = ingestion_integration_container.load_offers_usecase()
        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.CORPS},
        )

        with pytest.raises(InvalidDocumentTypeError):
            await usecase.execute(input_data)

    @pytest.mark.httpx_mock
    async def test_stops_when_fetch_by_type_returns_no_documents(
        self, db, httpx_mock, ingestion_integration_container
    ):
        usecase = ingestion_integration_container.load_offers_usecase()
        client = ingestion_integration_container.talentsoft_front_client()
        client.cached_token = cached_token()

        mock_offersummaries_response(client, httpx_mock, count_offers=0)

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.OFFERS},
        )

        with patch.object(
            usecase.document_repository,
            "find_by_external_ids",
            wraps=usecase.document_repository.find_by_external_ids,
        ) as repository_find_by_external_ids:
            result = await usecase.execute(input_data)

        repository_find_by_external_ids.assert_not_called()
        assert result == {"created": 0, "updated": 0, "errors": []}

    async def test_stops_after_max_iterations(
        self, db, httpx_mock, ingestion_integration_container
    ):
        usecase = ingestion_integration_container.load_offers_usecase()
        client = ingestion_integration_container.talentsoft_front_client()
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
            await usecase.execute(input_data)

        # (MAX_ITERATIONS - 1) * (getsummaries + getoffer calls)
        assert len(httpx_mock.get_requests()) == (MAX_ITERATIONS - 1) * 2

    async def test_stops_after_max_pages(
        self, db, httpx_mock, ingestion_integration_container
    ):
        usecase = ingestion_integration_container.load_offers_usecase()
        client = ingestion_integration_container.talentsoft_front_client()
        client.cached_token = cached_token()

        max_pages = 2
        for start in range(1, max_pages + 1):
            mock_offersummaries_response(
                client, httpx_mock, start=start, count_offers=1, has_more=True
            )
        mock_detail_offer_response(client, httpx_mock)

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.OFFERS, "max_pages": max_pages},
        )

        await usecase.execute(input_data)

        # max_pages * (offersummaries + getoffer)
        assert len(httpx_mock.get_requests()) == max_pages * 2
