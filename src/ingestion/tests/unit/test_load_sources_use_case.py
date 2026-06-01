from unittest.mock import AsyncMock, MagicMock

import pytest
from faker import Faker

from application.use_cases.load_sources import LoadSourcesUseCase
from domain.gateways.sources_gateway import ISourcesGateway
from domain.repositories.sources_repository import ISourcesRepository
from domain.source import Source

fake = Faker()


def _make_source(**kwargs) -> Source:
    defaults = {
        "source_id": "aaaa-bbbb",
        "type": "talentsoft",
        "client_id_back": "client-back-1",
        "client_id_front": "client-front-1",
        "base_url_front": fake.url(),
        "base_url_back": fake.url(),
    }
    return Source(**{**defaults, **kwargs})


@pytest.mark.asyncio
async def test_execute_loads_sources_into_repository():
    source = _make_source()
    mock_gateway = MagicMock(spec=ISourcesGateway)
    mock_gateway.fetch_sources = AsyncMock(return_value=[source])
    mock_repository = MagicMock(spec=ISourcesRepository)

    use_case = LoadSourcesUseCase(
        sources_gateway=mock_gateway, repository=mock_repository
    )
    await use_case.execute()

    mock_repository.load.assert_called_once_with([source])


@pytest.mark.asyncio
async def test_execute_raises_when_gateway_fails():
    mock_gateway = MagicMock(spec=ISourcesGateway)
    mock_gateway.fetch_sources = AsyncMock(side_effect=Exception("Gateway error"))
    mock_repository = MagicMock(spec=ISourcesRepository)

    use_case = LoadSourcesUseCase(
        sources_gateway=mock_gateway, repository=mock_repository
    )

    with pytest.raises(Exception, match="Gateway error"):
        await use_case.execute()

    mock_repository.load.assert_not_called()
