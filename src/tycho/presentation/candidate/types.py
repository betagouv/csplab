"""Shared presentation types for candidate module."""

from typing import TypedDict


class _BaseCard(TypedDict):
    """Shared fields for all result cards."""

    opportunity_type: str
    title: str
    description: str
    category: str
    category_value: str
    versant: str
    versant_value: str
    url: str


class ConcoursCard(_BaseCard):
    """Card data for a concours result."""

    access_modalities: list[str]


class OfferCard(_BaseCard):
    """Card data for an offer result."""

    location: str
    location_value: str
    contract_type_display: str


OpportunityCard = ConcoursCard | OfferCard
