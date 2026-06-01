import httpx

from domain.source import Source


class WebSourcesGateway:
    def __init__(self, client: httpx.AsyncClient, base_url: str, api_key: str) -> None:
        self._client = client
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key

    async def fetch_sources(self) -> list[Source]:
        url = f"{self._base_url}/api/v1/sources/"
        response = await self._client.get(
            url,
            headers={"Authorization": f"Api-Key {self._api_key}"},
        )
        response.raise_for_status()
        return [Source(**item) for item in response.json()]
