from unittest.mock import AsyncMock, MagicMock

import pytest

from application.usecases.publish_talentsoft_organisations import (
    PublishTalentsoftOrganisationsCommand,
    PublishTalentsoftOrganisationsUsecase,
)
from domain.gateways.publish_talentsoft_organismes_gateway import (
    IPublishTalentsoftOrganismesGateway,
)
from infrastructure.external_gateways.dtos.talentsoft_dtos import (
    TalentsoftOrganisationPayload,
)


def _organisation(code: int = 1) -> TalentsoftOrganisationPayload:
    return TalentsoftOrganisationPayload(
        entityCode=str(code), name="Mairie de Test", code=code
    )


@pytest.fixture
def mock_gateway():
    gateway = MagicMock(spec=IPublishTalentsoftOrganismesGateway)
    gateway.publish = AsyncMock()
    return gateway


@pytest.fixture
def usecase(mock_gateway):
    return PublishTalentsoftOrganisationsUsecase(
        publish_talentsoft_organismes_gateway=mock_gateway,
    )


@pytest.mark.asyncio
async def test_execute_publishes_each_batch(usecase, mock_gateway):
    batch_1 = [_organisation(code) for code in range(100)]
    batch_2 = [_organisation(code) for code in range(100, 150)]

    await usecase.execute(
        PublishTalentsoftOrganisationsCommand(batches=[batch_1, batch_2])
    )

    assert mock_gateway.publish.await_count == 2
    calls = mock_gateway.publish.await_args_list
    assert calls[0].args[0] == batch_1
    assert calls[1].args[0] == batch_2


@pytest.mark.asyncio
async def test_execute_does_not_rebatch(usecase, mock_gateway):
    batches = [[_organisation(code) for code in range(150)]]

    await usecase.execute(PublishTalentsoftOrganisationsCommand(batches=batches))

    mock_gateway.publish.assert_awaited_once_with(batches[0])


@pytest.mark.asyncio
async def test_execute_does_nothing_when_no_batches(usecase, mock_gateway):
    await usecase.execute(PublishTalentsoftOrganisationsCommand(batches=[]))

    mock_gateway.publish.assert_not_awaited()


@pytest.mark.asyncio
async def test_execute_propagates_gateway_error(usecase, mock_gateway):
    mock_gateway.publish.side_effect = RuntimeError("API down")

    with pytest.raises(RuntimeError, match="API down"):
        await usecase.execute(
            PublishTalentsoftOrganisationsCommand(batches=[[_organisation()]])
        )
