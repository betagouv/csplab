from unittest.mock import AsyncMock, MagicMock

import pytest

from application.usecases.load_metiers_multi_domaines import (
    LoadMetiersMultiDomainesUsecase,
)


@pytest.mark.asyncio
async def test_execute_loads_metiers_multi_domaines():
    gateway = MagicMock()
    gateway.fetch_metiers_multi_domaines = AsyncMock(return_value={"ERJUS008"})
    metiers_multi_domaines: set[str] = set()

    await LoadMetiersMultiDomainesUsecase(gateway, metiers_multi_domaines).execute()

    assert metiers_multi_domaines == {"ERJUS008"}
