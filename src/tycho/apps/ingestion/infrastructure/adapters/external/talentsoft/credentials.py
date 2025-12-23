"""
Credential parsing helpers.

TalentSoft token endpoint requires:
- grant_type
- client_id
- client_secret

Our config currently contains only `TalentSoftConfig.api_key`, so we support:
1) "<client_id>:<client_secret>" or "<client_id>|<client_secret>"
2) "grant_type=client_credentials&client_id=XXX&client_secret=YYY"
3) env vars TALENTSOFT_CLIENT_ID / TALENTSOFT_CLIENT_SECRET
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional, Tuple
from urllib.parse import parse_qs


@dataclass(frozen=True)
class TalentSoftCredentials:
    """Typed representation of TalentSoft OAuth credentials."""

    client_id: str
    client_secret: str
    grant_type: str = "client_credentials"


def _from_env() -> Optional[TalentSoftCredentials]:
    client_id = (os.getenv("TALENTSOFT_CLIENT_ID") or "").strip()
    client_secret = (os.getenv("TALENTSOFT_CLIENT_SECRET") or "").strip()
    if client_id and client_secret:
        return TalentSoftCredentials(client_id=client_id, client_secret=client_secret)
    return None


def _from_api_key_as_querystring(api_key: str) -> Optional[TalentSoftCredentials]:
    # Example: "grant_type=client_credentials&client_id=XXX&client_secret=YYY"
    if "client_id=" not in api_key or "client_secret=" not in api_key:
        return None

    parsed = parse_qs(api_key, keep_blank_values=True)
    client_id = (parsed.get("client_id", [""])[0] or "").strip()
    client_secret = (parsed.get("client_secret", [""])[0] or "").strip()
    grant_type = (parsed.get("grant_type", ["client_credentials"])[0] or "client_credentials").strip()

    if client_id and client_secret:
        return TalentSoftCredentials(client_id=client_id, client_secret=client_secret, grant_type=grant_type)
    return None


def _from_api_key_as_pair(api_key: str) -> Optional[TalentSoftCredentials]:
    # Example: "<client_id>:<client_secret>" or "<client_id>|<client_secret>"
    for sep in (":", "|"):
        if sep in api_key:
            left, right = api_key.split(sep, 1)
            client_id = left.strip()
            client_secret = right.strip()
            if client_id and client_secret:
                return TalentSoftCredentials(client_id=client_id, client_secret=client_secret)
    return None


def parse_credentials(api_key: str) -> TalentSoftCredentials:
    """
    Parse credentials from config.api_key or environment.

    Raises ValueError if nothing usable is found.
    """
    api_key = (api_key or "").strip()

    # 1) Postman-like querystring payload stored in api_key
    from_qs = _from_api_key_as_querystring(api_key)
    if from_qs:
        return from_qs

    # 2) "<id>:<secret>" stored in api_key
    from_pair = _from_api_key_as_pair(api_key)
    if from_pair:
        return from_pair

    # 3) Environment fallback
    from_env = _from_env()
    if from_env:
        return from_env

    raise ValueError(
        "Missing TalentSoft OAuth credentials. Provide either:\n"
        "- TalentSoftConfig.api_key as '<client_id>:<client_secret>' (or '|')\n"
        "- OR TalentSoftConfig.api_key as 'grant_type=client_credentials&client_id=...&client_secret=...'\n"
        "- OR env vars TALENTSOFT_CLIENT_ID and TALENTSOFT_CLIENT_SECRET"
    )
