from typing import Any

import httpx

_API_PREFIX = "/api/v1"


class BaseWebGateway:
    def __init__(self, client: httpx.AsyncClient, base_url: str, api_key: str) -> None:
        self._client = client
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key

    @property
    def _auth_headers(self) -> dict[str, str]:
        return {"Authorization": f"Api-Key {self._api_key}"}

    async def _get(self, path: str) -> httpx.Response:
        response = await self._client.get(
            f"{self._base_url}{_API_PREFIX}{path}",
            headers=self._auth_headers,
        )
        response.raise_for_status()
        return response

    async def _post(self, path: str, json: Any) -> httpx.Response:
        response = await self._client.post(
            f"{self._base_url}{_API_PREFIX}{path}",
            json=json,
            headers=self._auth_headers,
        )
        response.raise_for_status()
        return response
