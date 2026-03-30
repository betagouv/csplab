import re
from datetime import datetime, timezone
from typing import Optional
from unittest.mock import MagicMock, patch

import pytest

from application.ingestion.interfaces.load_documents_input import LoadDocumentsInput
from application.ingestion.interfaces.load_operation_type import LoadOperationType
from application.ingestion.usecases import load_offers
from domain.entities.document import Document, DocumentType
from domain.exceptions.document_error import InvalidDocumentTypeError
from tests.external_gateways.utils import (
    cached_token,
    offers_response,
)
from tests.factories.talentsoft_factories import TalentsoftDetailOfferFactory

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
    def test_raises_for_non_offers_type(
        self, db, httpx_mock, ingestion_integration_container
    ):
        usecase = ingestion_integration_container.load_offers_usecase()
        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.CORPS},
        )

        with pytest.raises(InvalidDocumentTypeError):
            usecase.execute(input_data)

    @pytest.mark.httpx_mock
    def test_stops_when_fetch_by_type_returns_no_documents(
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
            result = usecase.execute(input_data)

        repository_find_by_external_ids.assert_not_called()
        assert result == {"created": 0, "updated": 0, "errors": []}

    def test_stops_after_max_iterations(
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
            usecase.execute(input_data)

        # (MAX_ITERATIONS - 1) * (getsummaries + getoffer calls)
        assert len(httpx_mock.get_requests()) == (MAX_ITERATIONS - 1) * 2

    @pytest.mark.parametrize("reload", [False, True])
    def test_upsert_new_or_recently_updated_documents_only(
        self, db, httpx_mock, ingestion_integration_container, reload
    ):
        usecase = ingestion_integration_container.load_offers_usecase()
        document_repository = ingestion_integration_container.document_repository()
        client = ingestion_integration_container.talentsoft_front_client()
        client.cached_token = cached_token()

        new_offer, recently_modified_offer, modified_offer = (
            TalentsoftDetailOfferFactory.build().model_dump() for _ in range(3)
        )

        document_repository.upsert_batch(
            [make_document(o) for o in [recently_modified_offer, modified_offer]],
            DocumentType.OFFERS,
        )

        recently_modified_offer["modificationDate"] = format_modification_date(
            datetime.now(timezone.utc)
        )
        offers = [new_offer, recently_modified_offer, modified_offer]

        nb_pages = 3 if reload else 2
        for start in range(1, nb_pages + 1):
            mock_offersummaries_response(
                client,
                httpx_mock,
                start=start,
                count_offers=len(offers),
                has_more=True,
                offers=offers,
            )
        if reload:
            mock_offersummaries_response(
                client, httpx_mock, start=nb_pages + 1, count_offers=0
            )

        mock_detail_offer_response(client, httpx_mock, offer=new_offer)
        mock_detail_offer_response(client, httpx_mock, offer=recently_modified_offer)
        usecase.logger = MagicMock()

        input_data = LoadDocumentsInput(
            operation_type=LoadOperationType.FETCH_FROM_API,
            kwargs={"document_type": DocumentType.OFFERS, "reload": reload},
        )

        result = usecase.execute(input_data)
        assert result == {"created": 1, "updated": 1, "errors": []}

        if reload:
            for i in range(2, 4):
                usecase.logger.info.assert_any_call(
                    "LoadOffers, page %d, everything seems to be up-to-date… "
                    "CONTINUING (reload=True)",
                    i,
                )
        else:
            usecase.logger.info.assert_any_call(
                "LoadOffers, page %d, everything seems to be up-to-date… "
                "STOPPING iterations",
                2,
            )
