from unittest.mock import MagicMock

import pytest

from application.use_cases.clean_raw_offer import CleanRawOfferUseCase
from domain.entities.offer import Offer
from domain.entities.raw_offer import RawOffer
from domain.gateways.offers_cleaner import IOffersCleaner
from tests.factories.talentsoft_factories import TalentsoftDetailOfferFactory

REFERENCE = "2024-OFFER-001"
SOURCE_ID = "11111111-2222-3333-4444-555555555555"


@pytest.fixture
def raw_offer_with_data() -> RawOffer:
    offer_dto = TalentsoftDetailOfferFactory.build(reference=REFERENCE)
    return RawOffer(
        reference=REFERENCE,
        source_id=SOURCE_ID,
        data=offer_dto.model_dump(),
    )


@pytest.fixture
def mock_offers_cleaner():
    cleaner = MagicMock(spec=IOffersCleaner)
    return cleaner


@pytest.fixture
def use_case(mock_offers_cleaner) -> CleanRawOfferUseCase:
    return CleanRawOfferUseCase(offers_cleaner=mock_offers_cleaner)


def test_execute_calls_offers_cleaner(
    use_case, mock_offers_cleaner, raw_offer_with_data
):
    mock_offers_cleaner.clean.return_value = MagicMock(spec=Offer)

    use_case.execute(raw_offer_with_data)

    mock_offers_cleaner.clean.assert_called_once_with(raw_offer_with_data)


def test_execute_returns_cleaned_offer(
    use_case, mock_offers_cleaner, raw_offer_with_data
):
    expected_offer = MagicMock(spec=Offer)
    mock_offers_cleaner.clean.return_value = expected_offer

    result = use_case.execute(raw_offer_with_data)

    assert result is expected_offer


def test_execute_propagates_cleaner_errors(
    use_case, mock_offers_cleaner, raw_offer_with_data
):
    mock_offers_cleaner.clean.side_effect = ValueError("Invalid offer data")

    with pytest.raises(ValueError, match="Invalid offer data"):
        use_case.execute(raw_offer_with_data)
