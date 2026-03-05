"""Shared presentation types for candidate module."""

from typing import TypedDict


class FilterOption(TypedDict):
    """Typed structure for filter dropdown options."""

    value: str
    text: str


class _BaseCard(TypedDict):
    """Shared fields for all result cards."""

    opportunity_type: str
    opportunity_type_display: str
    title: str
    description: str
    category_display: str
    category_value: str
    versant_display: str
    versant_value: str
    url: str


class ConcoursCard(_BaseCard):
    """Card data for a concours result."""

    concours_id: str
    access_modalities: list[str]


class OfferCard(_BaseCard):
    """Card data for an offer result."""

    offer_id: str
    profile: str
    location: str
    location_value: str
    contract_type_display: str


OpportunityCard = ConcoursCard | OfferCard


class AccordionItem(TypedDict):
    """Structure for a DSFR accordion item."""

    id: str
    title: str
    content: str


class DrawerContext(TypedDict):
    """Template context for an opportunity drawer."""

    title: str
    opportunity_type_display: str
    versant_display: str
    category_display: str
    url: str
    accordions: list[AccordionItem]
    cta_heading: str
    cta_label: str
