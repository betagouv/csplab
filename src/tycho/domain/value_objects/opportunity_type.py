"""Opportunity type value object."""

from enum import StrEnum


class OpportunityType(StrEnum):
    """Type of opportunity (concours or offer)."""

    OFFER = "offer"
    CONCOURS = "concours"
