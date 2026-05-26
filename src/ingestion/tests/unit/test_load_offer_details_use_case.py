from unittest.mock import AsyncMock, MagicMock

import pytest

from application.use_cases.load_offer_details import LoadOfferDetailsUseCase
from infrastructure.exceptions.exceptions import ExternalApiError
from tests.factories.talentsoft_factories import TalentsoftDetailOfferFactory

REFERENCE = "2024-OFFER-001"


@pytest.fixture
def mock_client():
    client = MagicMock()
    client.get_detail = AsyncMock()
    return client


@pytest.fixture
def use_case(mock_client) -> LoadOfferDetailsUseCase:
    return LoadOfferDetailsUseCase(talentsoft_client=mock_client)


@pytest.mark.asyncio
async def test_execute_calls_get_detail_and_returns_offer(use_case, mock_client):
    offer = TalentsoftDetailOfferFactory.build(reference=REFERENCE)
    mock_client.get_detail.return_value = offer

    result = await use_case.execute(reference=REFERENCE)

    mock_client.get_detail.assert_called_once_with(REFERENCE)
    assert result == offer


@pytest.mark.asyncio
async def test_execute_propagates_external_api_error(use_case, mock_client):
    mock_client.get_detail.side_effect = ExternalApiError(
        message="Offer not found for reference: unknown-ref",
        api_name="Talentsoft Front API",
    )

    with pytest.raises(ExternalApiError, match="Offer not found for reference"):
        await use_case.execute(reference="unknown-ref")
