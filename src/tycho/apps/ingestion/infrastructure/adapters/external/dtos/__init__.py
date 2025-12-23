"""Ingestion infrastructure external adapters dtos."""
from .talentsoft_token_dto import CachedToken, TalentSoftTokenResponse
from .talentsoft_offer_summary_dto import TalentSoftOfferDocument

__all__ = [
    "TalentSoftTokenResponse",
    "CachedToken",
    "TalentSoftOfferDocument",
]
