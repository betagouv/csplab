"""Async HTTP client interface."""

from typing import Any, Dict, Optional, Protocol

from domain.types import JsonDataType


class IAsyncHttpResponse(Protocol):
    """HTTP response interface."""

    status_code: int
    text: str

    def json(self) -> JsonDataType:
        """Parse response as JSON."""
        ...

    def raise_for_status(self) -> None:
        """Raise exception for HTTP error status codes."""
        ...


class IAsyncHttpClient(Protocol):
    """Interface for async HTTP client operations."""

    async def __aenter__(self) -> "IAsyncHttpClient":
        """Async context manager entry."""
        ...

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        ...

    async def post(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        files: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[JsonDataType] = None,
    ) -> IAsyncHttpResponse:
        """Make an async POST request.

        Args:
            url: Request URL
            headers: Request headers
            files: Files to upload
            data: Form data
            json: JSON data

        Returns:
            HTTP response
        """
        ...

    async def get(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> IAsyncHttpResponse:
        """Make an async GET request.

        Args:
            url: Request URL
            headers: Request headers
            params: Query parameters

        Returns:
            HTTP response
        """
        ...
