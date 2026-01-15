"""HTTP client service implementation."""

import requests

from domain.services.http_client_interface import IHttpClient


class SyncHttpClient(IHttpClient):
    """Sync HTTP client wrapper with request implementation."""

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
