---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.18.1
  kernelspec:
    display_name: CSPLab Base (pandas, numpy, matplotlib)
    language: python
    name: csplab-base
---

## Imports

```python
import json
import os
import time
import logging
from typing import Any, Dict, Optional, Tuple, Protocol, runtime_checkable
from urllib.parse import parse_qs
from dataclasses import dataclass
import requests

from dotenv import load_dotenv


```

## Config

```python
load_dotenv()

TALENDSOFT_CLIENT_ID=os.getenv("TALENDSOFT_CLIENT_ID")
TALENDSOFT_CLIENT_SECRET=os.getenv("TALENDSOFT_CLIENT_SECRET")
TALENDSOFT_BASE_URL=os.getenv("TALENDSOFT_BASE_URL")

TALENDSOFT_BASE_URL, TALENDSOFT_CLIENT_ID, TALENDSOFT_CLIENT_SECRET
```

```python
session=requests.session()
```

## Exploration

```python jupyter={"source_hidden": true}
"""Logger service interface definitions."""

@runtime_checkable
class ILogger(Protocol):
    """Interface for logger service."""

    def get_logger(self, module_name: str) -> logging.Logger:
        """Get logger for specific module.

        Args:
            module_name: Module name for logger

        Returns:
            Configured logger instance
        """
        ...

    def info(self, message: str, *args: Any) -> None:
        """Log info message with automatic context capture."""
        ...

    def debug(self, message: str, *args: Any) -> None:
        """Log debug message with automatic context capture."""
        ...

    def warning(self, message: str, *args: Any) -> None:
        """Log warning message with automatic context capture."""
        ...

    def error(self, message: str, *args: Any) -> None:
        """Log error message with automatic context capture."""
        ...

```

```python jupyter={"source_hidden": true}
"""Logger service implementation."""

class LoggerService(ILogger):
    """Centralized logger service."""

    def __init__(self, name: str = "tycho"):
        """Initialize logger service.

        Args:
            name: Logger name
        """
        self.logger = logging.getLogger(name)

    def get_logger(self, module_name: str) -> logging.Logger:
        """Get logger for specific module.

        Args:
            module_name: Module name for logger

        Returns:
            Configured logger instance
        """
        return logging.getLogger(f"tycho.{module_name}")

    def info(self, message: str, *args: Any) -> None:
        """Log info message."""
        self.logger.info(message, *args)

    def debug(self, message: str, *args: Any) -> None:
        """Log debug message."""
        self.logger.debug(message, *args)

    def warning(self, message: str, *args: Any) -> None:
        """Log warning message."""
        self.logger.warning(message, *args)

    def error(self, message: str, *args: Any) -> None:
        """Log error message."""
        self.logger.error(message, *args)

```

```python
from pydantic import BaseModel, HttpUrl

class TalentSoftConfig(BaseModel):
    """Configuration for TalentSoft API client."""

    base_url: HttpUrl
    api_key: str
```

```python
"""Domain exceptions for TalentSoft integration."""


class TalentSoftApiError(RuntimeError):
    """Generic TalentSoft API error (network, unexpected payload, 4xx/5xx)."""


class TalentSoftAuthError(TalentSoftApiError):
    """Authentication-specific error (token retrieval, invalid credentials, 401)."""
```

```python
"""DTOs for TalentSoft token endpoint."""

@dataclass(frozen=True)
class TalentSoftTokenResponse:
    """Raw token response content."""

    access_token: str
    token_type: str
    expires_in: int
    refresh_token: Optional[str] = None


@dataclass
class CachedToken:
    """
    Cached token with an absolute expiry timestamp.

    `expires_at_epoch` is computed from now + expires_in.
    """

    access_token: str
    token_type: str
    expires_at_epoch: float
    refresh_token: Optional[str] = None

    def is_expired(self, leeway_seconds: int = 30) -> bool:
        """True if token is expired (with leeway)."""
        return time.time() >= (self.expires_at_epoch - leeway_seconds)
```

```python
config=TalentSoftConfig(base_url=TALENDSOFT_BASE_URL, api_key="")
config
```

```python
"""
Token service for TalentSoft.

Responsibilities:
- Call POST /api/token with body params: grant_type, client_id, client_secret
- Cache token in memory
- Refresh on expiry
"""

class TalentSoftTokenService:
    """Retrieve and cache OAuth2 access token for TalentSoft."""

    TOKEN_ENDPOINT = "api/token"

    def __init__(
        self,
        config: TalentSoftConfig,
        session: requests.Session,
        timeout: int = 30,
    ):
        self._config = config
        self._session = session
        self._timeout = timeout
        self._cached: Optional[CachedToken] = None

    # OVER ING
    def _build_url(self, endpoint: str) -> str:
        base = str(self._config.base_url).rstrip("/")
        path = endpoint.lstrip("/")
        return f"{base}/{path}"

    # USEFUL
    def get_access_token(self) -> CachedToken:
        """Return a valid cached token, fetching a new one if needed."""
        if self._cached is None or self._cached.is_expired():
            self._cached = self._fetch_token()
        return self._cached

    def force_refresh(self) -> CachedToken:
        """Force token refresh (used on 401 retry)."""
        self._cached = self._fetch_token()
        return self._cached

    def _fetch_token(self) -> CachedToken:
        """
        POST /api/token with x-www-form-urlencoded body:
          grant_type=client_credentials&client_id=XXX&client_secret=YYY
        """

        url = self._build_url(self.TOKEN_ENDPOINT)

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        # IMPORTANT: body parameters exactly as required
        data = {
            "grant_type": "client_credentials",
            "client_id": TALENDSOFT_CLIENT_ID,
            "client_secret": TALENDSOFT_CLIENT_SECRET,
        }

        print(f"Requesting TalentSoft token: POST {url}")

        try:
            response = self._session.post(url, headers=headers, data=data, timeout=self._timeout)
        except requests.RequestException as exc:
            raise TalentSoftAuthError(f"TalentSoft token request failed: {exc}") from exc

        if response.status_code >= 400:
            preview = (response.text or "")[:500]
            raise TalentSoftAuthError(f"TalentSoft token request failed: {response.status_code}")

        try:
            payload = response.json() if response.content else {}
        except ValueError:
            payload = {}

        access_token = str(payload.get("access_token") or "")
        token_type = str(payload.get("token_type") or "bearer")
        refresh_token = payload.get("refresh_token")

        expires_in_raw = payload.get("expires_in")
        try:
            expires_in = int(expires_in_raw)
        except (TypeError, ValueError):
            expires_in = 0

        if not access_token:
            raise TalentSoftAuthError("TalentSoft token response missing access_token")


        if expires_in <= 0:
            expires_in = 10 * 60

        token_response = TalentSoftTokenResponse(
            access_token=access_token,
            token_type=token_type,
            expires_in=expires_in,
            refresh_token=str(refresh_token) if refresh_token else None,
        )

        cached = CachedToken(
            access_token=token_response.access_token,
            token_type=token_response.token_type,
            expires_at_epoch=time.time() + token_response.expires_in,
            refresh_token=token_response.refresh_token,
        )

        print(f"TalentSoft token retrieved (expires_in={expires_in}s)")
        return cached
```

```python
cached_token = TalentSoftTokenService(config=config, session=session).get_access_token()
```

```python
cached_token.access_token, cached_token.token_type, cached_token.expires_at_epoch
```

```python
config.base_url
```

```python
OFFER_SUMMARIES_ENDPOINT = "/api/v2/offersummaries"
bearer_token = cached_token.access_token

url = f"{config.base_url}/{OFFER_SUMMARIES_ENDPOINT}"
headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {bearer_token}",
        }
params={"count": 1000}
resp = session.get(url, headers=headers, params=params)
```

```python
resp
```

```python
if resp.status_code == 401:
    print("offersummaries returned 401; refreshing token and retrying once.")
    token = bearer_token = cached_token.access_token.force_refresh()
    resp = self._offers_api.fetch(bearer_token=token.access_token, params=params)
```

```python
pagination = resp.json()['_pagination']
pagination
```

```python
from urllib.parse import urlparse, parse_qs

if pagination.get('hasMore', False ):
    next_url = next((link['href'] for link in pagination['links'] if link['rel'] == 'next'), None)
    parsed_url = urlparse(next_url)
    parsed_params = parse_qs(parsed_url.query)
    params = {k: v[0] for k, v in parsed_params.items()}
```

```python

params
```

```python
resp.json()['data'][0].keys()
```

```python
resp.json()['data'][0]
```

```python
class TalentSoftHttpClient:
    """Real TalentSoft client with token + endpoint-specific normalization."""

    OFFER_SUMMARIES_ENDPOINT = "/api/v2/offersummaries"

    def __init__(
        self,
        config: TalentSoftConfig,
        logger_service: ILogger,
        timeout: int = 30,
        session: Optional[requests.Session] = None,
    ):
        self._config = config
        self._logger = logger_service.get_logger("TalentSoftHttpClient")
        self._timeout = timeout
        self._session = session or requests.Session()

        self._token_service = TalentSoftTokenService(
            config=config,
            logger_service=logger_service,
            session=self._session,
            timeout=timeout,
        )
        self._offers_api = OfferSummariesApi(
            config=config,
            logger_service=logger_service,
            session=self._session,
            timeout=timeout,
        )

    # -------------------------
    # URL helpers
    # -------------------------

    def _build_url(self, endpoint: str) -> str:
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            return endpoint
        base = str(self._config.base_url).rstrip("/")
        path = endpoint.lstrip("/")
        return f"{base}/{path}"

    def _is_offersummaries(self, endpoint: str) -> bool:
        ep = endpoint.strip()
        if ep.startswith("http://") or ep.startswith("https://"):
            return ep.rstrip("/").endswith(self.OFFER_SUMMARIES_ENDPOINT.rstrip("/"))
        return ep.lstrip("/").rstrip("/").endswith(self.OFFER_SUMMARIES_ENDPOINT.lstrip("/").rstrip("/"))

    # -------------------------
    # Public API (compat)
    # -------------------------

    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """
        Main entrypoint used by the facade.

        If endpoint is /api/v2/offersummaries:
          - calls offersummaries api
          - maps payload to {"offers": [...]}
          - returns a Response containing normalized JSON

        Otherwise:
          - performs a raw request with Bearer token (no mapping)
        """
        method_upper = method.upper().strip()

        if self._is_offersummaries(endpoint):
            return self._request_offersummaries(params=kwargs.get("params"))

        # Default: raw request with bearer token
        token = self._token_service.get_access_token()
        headers = dict(kwargs.get("headers") or {})
        headers.setdefault("Accept", "application/json")
        headers["Authorization"] = f"Bearer {token.access_token}"

        url = self._build_url(endpoint)
        self._logger.info("TalentSoft API call: %s %s", method_upper, url)

        try:
            resp = self._session.request(
                method=method_upper,
                url=url,
                headers=headers,
                params=kwargs.get("params"),
                data=kwargs.get("data"),
                json=kwargs.get("json"),
                timeout=self._timeout,
            )
        except requests.RequestException as exc:
            self._logger.exception("TalentSoft request failed (network): %s %s", method_upper, url)
            raise TalentSoftApiError(f"TalentSoft request failed: {exc}") from exc

        # retry once on 401
        if resp.status_code == 401:
            self._logger.warning("401 received; refreshing token and retrying once.")
            token = self._token_service.force_refresh()
            headers["Authorization"] = f"Bearer {token.access_token}"

            resp = self._session.request(
                method=method_upper,
                url=url,
                headers=headers,
                params=kwargs.get("params"),
                data=kwargs.get("data"),
                json=kwargs.get("json"),
                timeout=self._timeout,
            )

        return resp

    # -------------------------
    # Offersummaries flow
    # -------------------------

    def _request_offersummaries(self, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        Full flow for /api/v2/offersummaries:
        - get token
        - call endpoint
        - retry once on 401
        - normalize JSON
        """
        token = self._token_service.get_access_token()
        resp = self._offers_api.fetch(bearer_token=token.access_token, params=params)

        if resp.status_code == 401:
            self._logger.warning("offersummaries returned 401; refreshing token and retrying once.")
            token = self._token_service.force_refresh()
            resp = self._offers_api.fetch(bearer_token=token.access_token, params=params)

        if resp.status_code >= 400:
            preview = (resp.text or "")[:500]
            self._logger.error("offersummaries failed: %s - %s", resp.status_code, preview)
            raise TalentSoftApiError(f"TalentSoft offersummaries failed: {resp.status_code}")

        # Normalize content to {"offers":[...]}
        return self._normalize_offersummaries_response(resp)

    def _normalize_offersummaries_response(self, upstream: requests.Response) -> requests.Response:
        """Create a new Response that contains the normalized payload."""
        try:
            payload = upstream.json() if upstream.content else {}
        except ValueError:
            payload = {}

        normalized = OfferSummariesMapper.map_payload(payload)
        offers_count = len(normalized.get("offers") or [])
        self._logger.info("Normalized offersummaries payload: %s offers", offers_count)

        # Build a new response to avoid side effects on the upstream response object
        new_resp = requests.Response()
        new_resp.status_code = upstream.status_code
        new_resp.headers = dict(upstream.headers)
        new_resp.encoding = "utf-8"
        new_resp._content = json.dumps(normalized, ensure_ascii=False).encode("utf-8")
        new_resp.headers["Content-Type"] = "application/json; charset=utf-8"
        new_resp.url = upstream.url

        return new_resp
```

```python
"""
Pure API layer for /api/v2/offersummaries.

Responsibilities:
- Execute the GET request with proper Authorization header
- No mapping / no business transformation
"""

class OfferSummariesApi:
    """HTTP calls for TalentSoft offer summaries."""

    ENDPOINT = "/api/v2/offersummaries"

    def __init__(
        self,
        config: TalentSoftConfig,
        logger_service: ILogger,
        session: requests.Session,
        timeout: int = 30,
    ):
        self._config = config
        self._logger = logger_service.get_logger("OfferSummariesApi")
        self._session = session
        self._timeout = timeout

    def _build_url(self) -> str:
        base = str(self._config.base_url).rstrip("/")
        path = self.ENDPOINT.lstrip("/")
        return f"{base}/{path}"

    def fetch(self, bearer_token: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """GET /api/v2/offersummaries with Bearer token."""
        url = self._build_url()
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {bearer_token}",
        }

        self._logger.info("TalentSoft offersummaries call: GET %s", url)

        try:
            return self._session.get(url, headers=headers, params=params, timeout=self._timeout)
        except requests.RequestException as exc:
            self._logger.exception("TalentSoft offersummaries request failed (network)")
            raise TalentSoftApiError(f"TalentSoft offersummaries request failed: {exc}") from exc
```

## Testing

```python
class DummyLoggerService(ILogger):
    def get_logger(self, name: str):
        import logging
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(name)
```

```python
config = TalentSoftConfig(base_url=TALENDSOFT_BASE_URL, api_key=api_key)
client = TalentSoftHttpClient(config=config, logger_service=DummyLoggerService(), timeout=30)
```

```python
    resp = client.request("GET", "/api/v2/offersummaries")
    print("Status:", resp.status_code)
    resp.raise_for_status()
    payload = resp.json()

    print("Normalized keys:", list(payload.keys()))
    offers = payload.get("offers") or []
    print("Normalized offers count:", len(offers))
    if offers:
        first = offers[0]
        print("First normalized offer:")
        for k, v in first.items():
            print(f"  {k}: {v}")
```
