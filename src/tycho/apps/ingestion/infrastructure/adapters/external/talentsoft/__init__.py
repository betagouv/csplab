"""TalentSoft integration package (token, api calls, mapping)."""

from .client import TalentSoftHttpClient
from .exceptions import TalentSoftApiError, TalentSoftAuthError

__all__ = ["TalentSoftHttpClient", "TalentSoftApiError", "TalentSoftAuthError"]
