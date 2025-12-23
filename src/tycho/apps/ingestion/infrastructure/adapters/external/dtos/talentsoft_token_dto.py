"""DTOs for TalentSoft token endpoint."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Optional


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
