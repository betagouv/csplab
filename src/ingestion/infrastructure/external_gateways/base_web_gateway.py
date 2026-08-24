from typing import Any

import httpx
from pydantic import BaseModel, Field, HttpUrl

_API_PREFIX = "/api/v1"


class WebGatewayCredentials(BaseModel):
    base_url: HttpUrl
    api_key: str = Field(min_length=1)

    @property
    def base_url_str(self) -> str:
        return str(self.base_url).rstrip("/")


class BaseWebGateway:
    def __init__(
        self, client: httpx.AsyncClient, credentials: WebGatewayCredentials
    ) -> None:
        self._client = client
        self._base_url = credentials.base_url_str
        self._api_key = credentials.api_key

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
