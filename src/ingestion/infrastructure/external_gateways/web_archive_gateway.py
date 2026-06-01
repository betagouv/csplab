import httpx


class WebArchiveGateway:
    def __init__(self, client: httpx.AsyncClient, base_url: str, api_key: str) -> None:
        self._client = client
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key

    async def archive(self, reference: str, source_id: str) -> None:
        url = f"{self._base_url}/api/v1/offres/archiver"
        response = await self._client.post(
            url,
            json={"reference": reference, "source_id": source_id},
            headers={"Authorization": f"Api-Key {self._api_key}"},
        )
        response.raise_for_status()
