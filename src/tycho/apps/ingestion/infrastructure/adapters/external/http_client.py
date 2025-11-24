"""HTTP client service implementation."""

from typing import Any, Protocol

import requests


class IHttpClient(Protocol):
    """Interface for HTTP client."""

    def request(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        """Make HTTP request.

        Args:
            method: HTTP method
            url: Request URL
            **kwargs: Additional request parameters

        Returns:
            HTTP response
        """
        ...


class HttpClient(IHttpClient):
    """HTTP client wrapper."""

    def __init__(self, timeout: int = 30):
        """Initialize HTTP client.

        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.session = requests.Session()

    def request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make HTTP request.

        Args:
            method: HTTP method
            url: Request URL
            **kwargs: Additional request parameters

        Returns:
            HTTP response
        """
        kwargs.setdefault("timeout", self.timeout)
        return self.session.request(method, url, **kwargs)
