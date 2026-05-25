from unittest.mock import AsyncMock, MagicMock

import pytest

from application.use_cases.load_offer_details import LoadOfferDetailsUseCase
from infrastructure.exceptions.exceptions import ExternalApiError
from infrastructure.external_gateways.dtos.talentsoft_dtos import (
    TalentsoftCodedObject,
    TalentsoftDetailOffer,
)

REFERENCE = "2024-OFFER-001"


def _make_detail_offer(reference: str = REFERENCE) -> TalentsoftDetailOffer:
    coded_object = TalentsoftCodedObject(
        code=1,
        clientCode="CODE",
        label="Label",
        active=True,
        type="type",
        parentType="",
    )
    return TalentsoftDetailOffer(
        reference=reference,
        isTopOffer=False,
        title="Software Engineer",
        organisationName="ACME Corp",
        organisationDescription="A great company",
        organisationLogoUrl="https://example.com/logo.png",
        modificationDate="2024-01-01",
        startPublicationDate="2024-01-01",
        offerUrl="https://example.com/offer",
        offerFamilyCategory=coded_object,
        contractTypeCountry=coded_object,
    )


@pytest.fixture
def mock_client():
    client = MagicMock()
    client.get_detail = AsyncMock()
    return client


@pytest.fixture
def use_case(mock_client) -> LoadOfferDetailsUseCase:
    return LoadOfferDetailsUseCase(talentsoft_client=mock_client)


@pytest.mark.asyncio
async def test_execute_calls_get_detail_with_reference(use_case, mock_client):
    offer = _make_detail_offer()
    mock_client.get_detail.return_value = offer

    result = await use_case.execute(reference=REFERENCE)

    mock_client.get_detail.assert_called_once_with(REFERENCE)
    assert result == offer


@pytest.mark.asyncio
async def test_execute_returns_detail_offer(use_case, mock_client):
    offer = _make_detail_offer(reference="REF-XYZ")
    mock_client.get_detail.return_value = offer

    result = await use_case.execute(reference="REF-XYZ")

    assert result.reference == "REF-XYZ"
    assert result.title == "Software Engineer"


@pytest.mark.asyncio
async def test_execute_propagates_external_api_error(use_case, mock_client):
    mock_client.get_detail.side_effect = ExternalApiError(
        message="Offer not found for reference: unknown-ref",
        api_name="Talentsoft Front API",
    )

    with pytest.raises(ExternalApiError, match="Offer not found for reference"):
        await use_case.execute(reference="unknown-ref")
