from unittest.mock import AsyncMock, MagicMock, Mock

import httpx
import pytest

from application.interfaces.sources_registry import ISourcesRegistry
from application.use_cases.load_sources import LoadSourcesUseCase
from tests.shared_fixtures import WEB_API_KEY, WEB_BASE_URL

SOURCES_URL = f"{WEB_BASE_URL}/api/data/sources/"


@pytest.mark.asyncio
async def test_execute_loads_sources_into_registry():
    sources_data = [
        {
            "source_id": "aaaa-bbbb",
            "type": "talentsoft",
            "client_id_back": "client-back-1",
            "client_id_front": "client-front-1",
            "base_url_front": "https://front.talentsoft.com",
            "base_url_back": "https://back.talentsoft.com",
        }
    ]
    mock_response = Mock()
    mock_response.json.return_value = sources_data

    mock_client = MagicMock(spec=httpx.AsyncClient)
    mock_client.get = AsyncMock(return_value=mock_response)
    mock_registry = MagicMock(spec=ISourcesRegistry)

    use_case = LoadSourcesUseCase(
        client=mock_client,
        web_base_url=WEB_BASE_URL,
        web_api_key=WEB_API_KEY,
        registry=mock_registry,
    )
    await use_case.execute()

    mock_registry.load.assert_called_once()
    loaded_sources = mock_registry.load.call_args[0][0]
    assert len(loaded_sources) == 1
    assert loaded_sources[0].source_id == "aaaa-bbbb"


@pytest.mark.asyncio
async def test_execute_raises_on_error_response():
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "500 Internal Server Error", request=Mock(), response=Mock()
    )

    mock_client = MagicMock(spec=httpx.AsyncClient)
    mock_client.get = AsyncMock(return_value=mock_response)
    mock_registry = MagicMock(spec=ISourcesRegistry)

    use_case = LoadSourcesUseCase(
        client=mock_client,
        web_base_url=WEB_BASE_URL,
        web_api_key=WEB_API_KEY,
        registry=mock_registry,
    )

    with pytest.raises(httpx.HTTPStatusError):
        await use_case.execute()
