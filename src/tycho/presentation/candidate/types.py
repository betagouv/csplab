from typing import TypedDict


class FilterOption(TypedDict):
    value: str
    text: str


class _BaseCard(TypedDict):
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
    concours_id: str
    access_modalities: list[str]


class OfferCard(_BaseCard):
    offer_id: str
    profile: str
    location: str
    location_value: str
    contract_type_display: str


OpportunityCard = ConcoursCard | OfferCard


class AccordionItem(TypedDict):
    id: str
    title: str
    content: str


class DrawerContext(TypedDict):
    title: str
    opportunity_id: str
    opportunity_type: str
    opportunity_type_display: str
    versant_display: str
    category_display: str
    url: str
    accordions: list[AccordionItem]
    cta_heading: str
    cta_label: str
