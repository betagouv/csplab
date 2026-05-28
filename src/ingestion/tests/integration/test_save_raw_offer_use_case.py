import logging
from unittest.mock import AsyncMock, MagicMock

import pytest
from faker import Faker
from pytest_httpx import HTTPXMock

from application.use_cases.load_offer_details import LoadOfferDetailsUseCase
from application.use_cases.save_raw_offer import SaveRawOfferUseCase
from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.external_gateways.talentsoft_client import (
    TalentsoftConfig,
    TalentsoftFrontClient,
)
from infrastructure.models.raw_offer import RawOffer
from tests.conftest import (
    SOURCE_ID,
    TALENTSOFT_FRONT_BASE_URL,
    TALENTSOFT_FRONT_CLIENT_ID,
    TALENTSOFT_FRONT_CLIENT_SECRET,
)
from tests.shared_fixtures import (
    TALENTSOFT_DETAIL_OFFER_URL,
    TALENTSOFT_TOKEN_URL,
    mock_talentsoft_token_response,
)
from tests.unit.external_gateways.utils import detail_offer_response

fake = Faker()
REFERENCE = fake.bothify("####-????-###", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")


@pytest.fixture
def talentsoft_front_client() -> TalentsoftFrontClient:
    return TalentsoftFrontClient(
        config=TalentsoftConfig(
            base_url=TALENTSOFT_FRONT_BASE_URL,
            client_id=TALENTSOFT_FRONT_CLIENT_ID,
            client_secret=TALENTSOFT_FRONT_CLIENT_SECRET,
        ),
        logger=logging.getLogger(__name__),
    )


@pytest.fixture
def mock_repository():
    repo = MagicMock()
    repo.upsert = AsyncMock()
    return repo


@pytest.fixture
def use_case(talentsoft_front_client, mock_repository) -> SaveRawOfferUseCase:
    return SaveRawOfferUseCase(
        load_offer_details=LoadOfferDetailsUseCase(
            talentsoft_client=talentsoft_front_client
        ),
        raw_offer_repository=mock_repository,
    )


@pytest.mark.asyncio
async def test_execute_fetches_offer_and_upserts_raw_offer(
    use_case, mock_repository, httpx_mock: HTTPXMock
):
    offer_data = detail_offer_response(reference=REFERENCE)
    mock_talentsoft_token_response(httpx_mock)
    httpx_mock.add_response(
        method="GET",
        url=f"{TALENTSOFT_DETAIL_OFFER_URL}?reference={REFERENCE}",
        json=offer_data,
    )

    await use_case.execute(reference=REFERENCE, source_id=SOURCE_ID)

    mock_repository.upsert.assert_called_once()
    saved: RawOffer = mock_repository.upsert.call_args[0][0]
    assert saved.reference == REFERENCE
    assert saved.source_id == SOURCE_ID
    assert saved.loaded_at is not None
    assert saved.error_msg is None
    assert saved.data is not None
    assert saved.data["reference"] == REFERENCE


@pytest.mark.asyncio
async def test_execute_upserts_error_msg_and_reraises_on_api_failure(
    use_case, mock_repository, httpx_mock: HTTPXMock
):
    mock_talentsoft_token_response(httpx_mock)
    # The client has max_retries=2, so it will attempt 3 GET requests total.
    for _ in range(3):
        httpx_mock.add_response(
            method="GET",
            url=f"{TALENTSOFT_DETAIL_OFFER_URL}?reference={REFERENCE}",
            status_code=500,
        )

    with pytest.raises(ExternalApiError):
        await use_case.execute(reference=REFERENCE, source_id=SOURCE_ID)

    mock_repository.upsert.assert_called_once()
    saved: RawOffer = mock_repository.upsert.call_args[0][0]
    assert saved.reference == REFERENCE
    assert saved.source_id == SOURCE_ID
    assert saved.loaded_at is None
    assert saved.data is None
    assert saved.error_msg is not None


@pytest.mark.asyncio
async def test_token_is_reused_across_executions(
    use_case, mock_repository, httpx_mock: HTTPXMock
):
    reference_2 = fake.bothify("####-????-###", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    mock_talentsoft_token_response(httpx_mock)
    httpx_mock.add_response(
        method="GET",
        url=f"{TALENTSOFT_DETAIL_OFFER_URL}?reference={REFERENCE}",
        json=detail_offer_response(reference=REFERENCE),
    )
    httpx_mock.add_response(
        method="GET",
        url=f"{TALENTSOFT_DETAIL_OFFER_URL}?reference={reference_2}",
        json=detail_offer_response(reference=reference_2),
    )

    await use_case.execute(reference=REFERENCE, source_id=SOURCE_ID)
    await use_case.execute(reference=reference_2, source_id=SOURCE_ID)

    token_requests = [
        r for r in httpx_mock.get_requests() if str(r.url) == TALENTSOFT_TOKEN_URL
    ]
    assert len(token_requests) == 1
    assert mock_repository.upsert.call_count == 2
