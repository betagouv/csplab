from django.utils.html import linebreaks
from django.utils.safestring import mark_safe

from domain.entities.concours import Concours
from domain.entities.offer import Offer
from domain.value_objects.opportunity_type import OpportunityType
from domain.value_objects.verse import Verse
from presentation.candidate.filter_config import (
    format_category_value,
    format_location_value,
)
from presentation.candidate.formatters import (
    format_category_display,
    format_contract_type_display,
    format_location_display,
    format_opportunity_type_display,
    format_verse_display,
)
from presentation.candidate.types import (
    AccordionItem,
    ConcoursCard,
    DrawerContext,
    OfferCard,
)


class ConcoursToTemplateMapper:
    @staticmethod
    def map_for_card(concours: Concours) -> ConcoursCard:
        return {
            "opportunity_type": OpportunityType.CONCOURS,
            "opportunity_type_display": format_opportunity_type_display(
                OpportunityType.CONCOURS
            ),
            "concours_id": str(concours.id),
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

    @staticmethod
    def map_for_drawer(concours: Concours) -> DrawerContext:
        accordions: list[AccordionItem] = []
        if concours.grade:
            accordions.append(
                {
                    "id": "drawer-grade-content",
                    "title": "Grade",
                    "content": mark_safe(  # noqa: S308
                        linebreaks(concours.grade, autoescape=True)
                    ),
                }
            )
        return {
            "title": concours.corps,
            "opportunity_type_display": format_opportunity_type_display(
                OpportunityType.CONCOURS
            ),
            "versant_display": format_verse_display(Verse.FPE),
            "category_display": format_category_display(concours.category),
            "url": "#",
            "accordions": accordions,
            "cta_heading": "Comment s'inscrire ?",
            "cta_label": "Voir le concours",
        }


class OfferToTemplateMapper:
    @staticmethod
    def map_for_card(offer: Offer) -> OfferCard:
        return {
            "opportunity_type": OpportunityType.OFFER,
            "opportunity_type_display": format_opportunity_type_display(
                OpportunityType.OFFER
            ),
            "title": offer.title,
            "description": offer.mission,
            "offer_id": str(offer.id),
            "profile": offer.profile,
            "category_display": format_category_display(offer.category),
            "category_value": format_category_value(offer.category),
            "versant_display": format_verse_display(offer.verse),
            "versant_value": offer.verse.value if offer.verse else "",
            "location": format_location_display(offer.localisation),
            "location_value": format_location_value(offer.localisation),
            "contract_type_display": format_contract_type_display(offer.contract_type),
            "url": str(offer.offer_url) if offer.offer_url else "#",
        }

    @staticmethod
    def map_for_drawer(offer: Offer) -> DrawerContext:
        accordions: list[AccordionItem] = []
        if offer.mission:
            accordions.append(
                {
                    "id": "drawer-mission-content",
                    "title": "Mission",
                    "content": mark_safe(  # noqa: S308
                        linebreaks(offer.mission, autoescape=True)
                    ),
                }
            )
        if offer.profile:
            accordions.append(
                {
                    "id": "drawer-profile-content",
                    "title": "Profil recherch\u00e9",
                    "content": mark_safe(  # noqa: S308
                        linebreaks(offer.profile, autoescape=True)
                    ),
                }
            )
        return {
            "title": offer.title,
            "opportunity_type_display": format_opportunity_type_display(
                OpportunityType.OFFER
            ),
            "versant_display": format_verse_display(offer.verse),
            "category_display": format_category_display(offer.category),
            "url": str(offer.offer_url) if offer.offer_url else "#",
            "accordions": accordions,
            "cta_heading": "Candidater à ce poste",
            "cta_label": "Voir l'offre",
        }
