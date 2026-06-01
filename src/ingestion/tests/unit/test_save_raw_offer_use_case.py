from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from application.use_cases.save_raw_offer import SaveRawOfferUseCase
from domain.gateways.offers_gateway import IOffersGateway
from domain.raw_offer import RawOffer
from infrastructure.exceptions.exceptions import ExternalApiError

REFERENCE = "2024-OFFER-001"
SOURCE_ID = "11111111-2222-3333-4444-555555555555"
RAW_DATA = {"reference": REFERENCE, "title": "Software Engineer"}
GATEWAY_OFFER = RawOffer(reference=REFERENCE, data=RAW_DATA)


@pytest.fixture
def mock_offers_gateway():
    client = MagicMock(spec=IOffersGateway)
    client.get_detail = AsyncMock()
    return client


@pytest.fixture
def mock_raw_offer_repository():
    repo = MagicMock()
    repo.upsert = AsyncMock()
    return repo


@pytest.fixture
def use_case(mock_offers_gateway, mock_raw_offer_repository) -> SaveRawOfferUseCase:
    return SaveRawOfferUseCase(
        offers_gateway=mock_offers_gateway,
        raw_offer_repository=mock_raw_offer_repository,
    )


@pytest.mark.asyncio
async def test_execute_calls_offers_gateway(
    use_case, mock_offers_gateway, mock_raw_offer_repository
):
    offer = GATEWAY_OFFER
    mock_offers_gateway.get_detail.return_value = offer

    await use_case.execute(reference=REFERENCE, source_id=SOURCE_ID)

    mock_offers_gateway.get_detail.assert_called_once_with(REFERENCE)


@pytest.mark.asyncio
async def test_execute_upserts_raw_offer_with_data_on_success(
    use_case, mock_offers_gateway, mock_raw_offer_repository
):
    offer = GATEWAY_OFFER
    mock_offers_gateway.get_detail.return_value = offer

    await use_case.execute(reference=REFERENCE, source_id=SOURCE_ID)

    mock_raw_offer_repository.upsert.assert_called_once()
    saved: RawOffer = mock_raw_offer_repository.upsert.call_args[0][0]
    assert saved.reference == REFERENCE
    assert saved.source_id == SOURCE_ID
    assert saved.loaded_at is not None
    assert saved.error_msg is None
    assert saved.data == offer.data


@pytest.mark.asyncio
async def test_execute_upserts_raw_offer_with_error_msg_on_failure(
    use_case, mock_offers_gateway, mock_raw_offer_repository
):
    error = ExternalApiError(message="Upstream error", api_name="Talentsoft Front API")
    mock_offers_gateway.get_detail.side_effect = error

    with pytest.raises(ExternalApiError):
        await use_case.execute(reference=REFERENCE, source_id=SOURCE_ID)

    mock_raw_offer_repository.upsert.assert_called_once()
    saved: RawOffer = mock_raw_offer_repository.upsert.call_args[0][0]
    assert saved.reference == REFERENCE
    assert saved.source_id == SOURCE_ID
    assert saved.loaded_at is None
    assert saved.data is None
    assert "Upstream error" in saved.error_msg


@pytest.mark.asyncio
async def test_execute_re_raises_original_error_when_upsert_also_fails(
    use_case, mock_offers_gateway, mock_raw_offer_repository
):
    original_error = ExternalApiError(
        message="Upstream error", api_name="Talentsoft Front API"
    )
    mock_offers_gateway.get_detail.side_effect = original_error
    mock_raw_offer_repository.upsert.side_effect = RuntimeError("DB unavailable")

    with pytest.raises(ExternalApiError, match="Upstream error"):
        await use_case.execute(reference=REFERENCE, source_id=SOURCE_ID)


@pytest.mark.asyncio
async def test_execute_does_not_raise_when_upsert_fails_after_success(
    use_case, mock_offers_gateway, mock_raw_offer_repository
):
    offer = GATEWAY_OFFER
    mock_offers_gateway.get_detail.return_value = offer
    mock_raw_offer_repository.upsert.side_effect = RuntimeError("DB unavailable")

    # Should not raise — the upsert error is swallowed and logged
    with patch("application.use_cases.save_raw_offer.logger") as mock_logger:
        await use_case.execute(reference=REFERENCE, source_id=SOURCE_ID)
        mock_logger.exception.assert_called_once()
