"""Async HTTP client implementation using httpx."""

from typing import Any, Dict, Optional

import httpx

from domain.services.async_http_client_interface import (
    IAsyncHttpClient,
    IAsyncHttpResponse,
)


class HttpxResponse(IAsyncHttpResponse):
    """Wrapper for httpx.Response to match HttpResponse protocol."""

    def __init__(self, response: httpx.Response):
        """Initialize with httpx response."""
        self._response = response
        self.status_code = response.status_code
        self.text = response.text

    def json(self) -> Dict[str, Any]:
        """Parse response as JSON."""
        return self._response.json()

    def raise_for_status(self) -> None:
        """Raise exception for HTTP error status codes."""
        self._response.raise_for_status()


class AsyncHttpClient(IAsyncHttpClient):
    """Async HTTP client implementation using httpx."""

    def __init__(self, timeout: int = 120):
        """Initialize the async HTTP client.

        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self) -> "AsyncHttpClient":
        """Async context manager entry."""
        self._client = httpx.AsyncClient(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()
            self._client = None

    async def post(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        files: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
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

        Raises:
            RuntimeError: If client is not initialized
        """
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
        params: Optional[Dict[str, Any]] = None,
    ) -> IAsyncHttpResponse:
        """Make an async GET request.

        Args:
            url: Request URL
            headers: Request headers
            params: Query parameters

        Returns:
            HTTP response

        Raises:
            RuntimeError: If client is not initialized
        """
        if not self._client:
            raise RuntimeError("Client not initialized. Use async context manager.")

        response = await self._client.get(
            url=url,
            headers=headers,
            params=params,
        )
        return HttpxResponse(response)
