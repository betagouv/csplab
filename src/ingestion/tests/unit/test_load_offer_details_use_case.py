import pytest

from application.use_cases.load_offer_details import LoadOfferDetailsUseCase
from infrastructure.exceptions.exceptions import ExternalApiError
from tests.factories.talentsoft_factories import TalentsoftDetailOfferFactory

REFERENCE = "2024-OFFER-001"


@pytest.mark.asyncio
async def test_execute_calls_get_detail_and_returns_offer(
    load_offer_details_use_case: LoadOfferDetailsUseCase, talentsoft_mock_client
):
    offer = TalentsoftDetailOfferFactory.build(reference=REFERENCE)
    talentsoft_mock_client.get_detail.return_value = offer

    result = await load_offer_details_use_case.execute(reference=REFERENCE)

    talentsoft_mock_client.get_detail.assert_called_once_with(REFERENCE)
    assert result == offer


@pytest.mark.asyncio
async def test_execute_propagates_external_api_error(
    load_offer_details_use_case: LoadOfferDetailsUseCase, talentsoft_mock_client
):
    talentsoft_mock_client.get_detail.side_effect = ExternalApiError(
        message="Offer not found for reference: unknown-ref",
        api_name="Talentsoft Front API",
    )

    with pytest.raises(ExternalApiError, match="Offer not found for reference"):
        await load_offer_details_use_case.execute(reference="unknown-ref")
