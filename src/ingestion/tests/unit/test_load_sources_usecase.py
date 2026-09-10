from unittest.mock import AsyncMock, MagicMock

import pytest

from application.usecases.load_sources import LoadSourcesUsecase
from domain.gateways.sources_gateway import ISourcesGateway
from domain.repositories.sources_repository import ISourcesRepository
from tests.factories.domain_factories import SourceFactory


@pytest.mark.asyncio
async def test_execute_loads_sources_into_repository():
    source = SourceFactory.build(source_id="aaaa-bbbb", slug="source-slug")
    mock_gateway = MagicMock(spec=ISourcesGateway)
    mock_gateway.fetch_sources = AsyncMock(return_value=[source])
    mock_repository = MagicMock(spec=ISourcesRepository)

    usecase = LoadSourcesUsecase(
        sources_gateway=mock_gateway, repository=mock_repository
    )
    await usecase.execute()

    mock_repository.load.assert_called_once_with([source])


@pytest.mark.asyncio
async def test_execute_raises_when_gateway_fails():
    mock_gateway = MagicMock(spec=ISourcesGateway)
    mock_gateway.fetch_sources = AsyncMock(side_effect=Exception("Gateway error"))
    mock_repository = MagicMock(spec=ISourcesRepository)

    usecase = LoadSourcesUsecase(
        sources_gateway=mock_gateway, repository=mock_repository
    )

    with pytest.raises(Exception, match="Gateway error"):
        await usecase.execute()

    mock_repository.load.assert_not_called()
