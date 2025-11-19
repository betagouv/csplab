"""HTTP client interface definitions."""

from typing import Any, Protocol

import requests

HTTP_OK = 200


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
