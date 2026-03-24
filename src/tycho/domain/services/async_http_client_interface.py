from typing import Any, Dict, Mapping, Optional, Protocol

from domain.types import JsonDataType


class IAsyncHttpResponse(Protocol):
    status_code: int
    text: str

    def json(self) -> JsonDataType: ...

    def raise_for_status(self) -> None: ...


class IAsyncHttpClient(Protocol):
    async def __aenter__(self) -> "IAsyncHttpClient": ...

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None: ...

    async def post(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        files: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[JsonDataType] = None,
    ) -> IAsyncHttpResponse: ...

    async def get(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Mapping[str, int | str]] = None,
    ) -> IAsyncHttpResponse: ...
