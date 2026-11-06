from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from application.usecases.load_metiers_multi_domaines import (
    LoadMetiersMultiDomainesUsecase,
)
from domain.gateways.metiers_gateway import IMetiersGateway
from infrastructure.metiers_multi_domaines_repository import (
    MetiersMultiDomainesRepository,
)


@pytest.mark.asyncio
async def test_execute_loads_codes_into_repository():
    gateway = MagicMock(spec=IMetiersGateway)
    gateway.fetch_metiers_multi_domaines = AsyncMock(return_value={"ERJUS008"})
    repository = MetiersMultiDomainesRepository()

    await LoadMetiersMultiDomainesUsecase(
        metiers_gateway=gateway, repository=repository
    ).execute()

    assert "ERJUS008" in repository
    assert "ERSEC031" not in repository


@pytest.mark.asyncio
async def test_execute_retries_transient_errors():
    gateway = MagicMock(spec=IMetiersGateway)
    gateway.fetch_metiers_multi_domaines = AsyncMock(
        side_effect=[httpx.ConnectError("refused"), {"ERTRA007"}]
    )
    repository = MetiersMultiDomainesRepository()

    await LoadMetiersMultiDomainesUsecase(
        metiers_gateway=gateway, repository=repository, base_delay_seconds=0
    ).execute()

    assert gateway.fetch_metiers_multi_domaines.await_count == 2
    assert "ERTRA007" in repository
