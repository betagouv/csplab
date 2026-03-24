from typing import Any, Dict, Mapping, Optional

import httpx

from domain.services.async_http_client_interface import (
    IAsyncHttpClient,
    IAsyncHttpResponse,
)
from domain.types import JsonDataType


class HttpxResponse(IAsyncHttpResponse):
    def __init__(self, response: httpx.Response):
        self._response = response
        self.status_code = response.status_code
        self.text = response.text

    def json(self) -> JsonDataType:
        return self._response.json()

    def raise_for_status(self) -> None:
        self._response.raise_for_status()


class AsyncHttpClient(IAsyncHttpClient):
    def __init__(self, timeout: int = 120):
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self) -> "AsyncHttpClient":
        self._client = httpx.AsyncClient(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None

    async def post(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        files: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[JsonDataType] = None,
    ) -> IAsyncHttpResponse:
        if not self._client:
            raise RuntimeError("Client not initialized. Use async context manager.")

        response = await self._client.post(
            url=url,
            headers=headers,
            files=files,
            data=data,
            json=json,
        )
        return HttpxResponse(response)

    async def get(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Mapping[str, int | str]] = None,
    ) -> IAsyncHttpResponse:
        if not self._client:
            raise RuntimeError("Client not initialized. Use async context manager.")

        response = await self._client.get(
            url=url,
            headers=headers,
            params=params,
        )
        return HttpxResponse(response)
