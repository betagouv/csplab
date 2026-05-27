from typing import Any, Dict, Mapping, Optional, Self

import httpx


class AsyncHttpClient:
    def __init__(self, timeout: int = 120):
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None

    def _ensure_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client

    async def __aenter__(self) -> Self:
        self._ensure_client()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None

    async def post(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> httpx.Response:
        return await self._ensure_client().post(url=url, headers=headers, data=data)

    async def get(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Mapping[str, int | str]] = None,
    ) -> httpx.Response:
        return await self._ensure_client().get(url=url, headers=headers, params=params)
