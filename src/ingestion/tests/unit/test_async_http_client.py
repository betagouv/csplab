import pytest
from pytest_httpx import HTTPXMock

from infrastructure.gateways.async_http_client import AsyncHttpClient


@pytest.mark.asyncio
async def test_post_without_context_manager_succeeds(httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="POST", url="https://example.com")
    client = AsyncHttpClient()
    response = await client.post("https://example.com")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_without_context_manager_succeeds(httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="GET", url="https://example.com")
    client = AsyncHttpClient()
    response = await client.get("https://example.com")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_aclose_cleans_up_client(httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="GET", url="https://example.com")
    async with AsyncHttpClient() as client:
        await client.get("https://example.com")
    assert client._client is None
