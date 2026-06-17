from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID

import pytest
from referentiel.value_objects.contract_type import ContractType
from referentiel.value_objects.verse import Verse

from application.use_cases.publish_offer import PublishOfferUseCase
from domain.entities.offer import Offer
from domain.gateways.publish_offer_gateway import IPublishOfferGateway
from domain.gateways.publish_offer_input import PublishOfferInput

OFFER = Offer(
    reference="2024-OFFER-001",
    source_id=UUID("11111111-2222-3333-4444-555555555555"),
    external_id="FPT-2024-OFFER-001",
    title="Software Engineer",
    profile="Profile text",
    mission="Mission text",
    organization="City Hall",
    verse=Verse.FPT,
    category=None,
    contract_type=ContractType.TITULAIRE_CONTRACTUEL,
    offer_url=None,
    application_url=None,
    localisation=None,
    publication_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
    end_publication_date=None,
    beginning_date=None,
    family_code="INF001",
)


@pytest.fixture
def mock_gateway():
    gateway = MagicMock(spec=IPublishOfferGateway)
    gateway.publish = AsyncMock()
    return gateway


@pytest.fixture
def use_case(mock_gateway):
    return PublishOfferUseCase(publish_offer_gateway=mock_gateway)


@pytest.mark.asyncio
async def test_execute_calls_gateway_publish(use_case, mock_gateway):
    await use_case.execute(OFFER)

    mock_gateway.publish.assert_awaited_once_with(
        PublishOfferInput(source_id=OFFER.source_id, offer=OFFER)
    )


@pytest.mark.asyncio
async def test_execute_propagates_gateway_error(use_case, mock_gateway):
    mock_gateway.publish.side_effect = RuntimeError("API down")

    with pytest.raises(RuntimeError, match="API down"):
        await use_case.execute(OFFER)
