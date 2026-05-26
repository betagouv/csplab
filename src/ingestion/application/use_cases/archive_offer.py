import httpx


class ArchiveOfferUseCase:
    def __init__(
        self,
        client: httpx.AsyncClient,
        web_base_url: str,
        web_api_key: str,
    ) -> None:
        self._client = client
        self._web_base_url = web_base_url
        self._web_api_key = web_api_key

    async def execute(self, reference: str, source_id: str) -> None:
        url = f"{self._web_base_url}/api/v1/offres/archiver"
        response = await self._client.post(
            url,
            json={"reference": reference, "source_id": source_id},
            headers={"Authorization": f"Api-Key {self._web_api_key}"},
        )
        response.raise_for_status()
