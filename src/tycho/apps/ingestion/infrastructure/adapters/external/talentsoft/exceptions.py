"""Domain exceptions for TalentSoft integration."""


class TalentSoftApiError(RuntimeError):
    """Generic TalentSoft API error (network, unexpected payload, 4xx/5xx)."""


class TalentSoftAuthError(TalentSoftApiError):
    """Authentication-specific error (token retrieval, invalid credentials, 401)."""
