"""Mapper for transforming Concours and Offer entities to template format."""

from domain.entities.concours import Concours
from domain.entities.offer import Offer
from domain.value_objects.verse import Verse
from presentation.candidate.filter_config import (
    format_category_value,
)
from presentation.candidate.formatters import (
    format_category_display,
    format_contract_type_display,
    format_verse_display,
)
from presentation.candidate.types import ConcoursCard, OfferCard


class ConcoursToTemplateMapper:
    """Maps Concours entities to template-compatible dictionaries."""

    @staticmethod
    def map(concours: Concours) -> ConcoursCard:
        """Transform a Concours entity to template format."""
        return {
            "opportunity_type": "concours",
            "title": concours.corps,
            "description": concours.grade,
            "access_modalities": [str(m) for m in concours.access_modality]
            if concours.access_modality
            else [],
            "category_display": format_category_display(concours.category),
            "category_value": format_category_value(concours.category),
            "versant_display": format_verse_display(Verse.FPE),
            "versant_value": Verse.FPE.value,
            "url": "#",
        }


class OfferToTemplateMapper:
    """Maps Offer entities to template-compatible dictionaries."""

    @staticmethod
    def map(offer: Offer) -> OfferCard:
        """Transform an Offer entity to template format."""
        return {
            "opportunity_type": "offer",
            "title": offer.title,
            "description": offer.mission,
            "location": OfferToTemplateMapper._format_location_display(
                offer.localisation
            ),
            "category_display": format_category_display(offer.category),
            "category_value": format_category_value(offer.category),
            "versant_display": format_verse_display(offer.verse),
            "versant_value": offer.verse.value if offer.verse else "",
            "contract_type_display": format_contract_type_display(offer.contract_type),
            "url": str(offer.offer_url) if offer.offer_url else "#",
        }

    @staticmethod
    def _format_location_display(localisation) -> str:
        """Format localisation for display."""
        if not localisation:
            return ""
        return f"{localisation.region}, {localisation.department}"
