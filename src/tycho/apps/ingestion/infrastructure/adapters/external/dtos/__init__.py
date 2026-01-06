"""Ingestion infrastructure external adapters dtos."""

from .talentsoft_offer_summary_dto import TalentSoftOfferDocument
from .talentsoft_token_dto import CachedToken, TalentSoftTokenResponse

__all__ = [
    "TalentSoftTokenResponse",
    "CachedToken",
    "TalentSoftOfferDocument",
]
