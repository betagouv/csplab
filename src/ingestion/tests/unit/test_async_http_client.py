import pytest

from infrastructure.gateways.async_http_client import AsyncHttpClient


@pytest.mark.asyncio
async def test_post_without_context_manager_raises():
    client = AsyncHttpClient()
    with pytest.raises(RuntimeError, match="Client not initialized"):
        await client.post("https://example.com")


@pytest.mark.asyncio
async def test_get_without_context_manager_raises():
    client = AsyncHttpClient()
    with pytest.raises(RuntimeError, match="Client not initialized"):
        await client.get("https://example.com")
