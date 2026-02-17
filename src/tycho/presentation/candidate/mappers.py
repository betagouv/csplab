"""Mapper for transforming Concours and Offer entities to template format."""

from domain.entities.concours import Concours
from domain.entities.offer import Offer
from domain.value_objects.category import Category
from domain.value_objects.contract_type import ContractType
from domain.value_objects.verse import Verse


class _BaseMapper:
    """Base mapper with shared formatting methods."""

    @staticmethod
    def _format_category_display(category: Category | None) -> str:
        """Format category for display (e.g., 'Catégorie A')."""
        if not category:
            return ""
        if category == Category.APLUS:
            return "Catégorie A"
        if category == Category.HORS_CATEGORIE:
            return "Hors catégorie"
        return f"Catégorie {category.value}"

    @staticmethod
    def _format_category_value(category: Category | None) -> str:
        """Format category value for filtering (lowercase)."""
        if not category:
            return ""
        if category == Category.APLUS:
            return Category.A.value.lower()
        if category == Category.HORS_CATEGORIE:
            return "hors_categorie"
        return category.value.lower()

    @staticmethod
    def _format_verse(verse: Verse | None) -> str:
        """Format verse value for display."""
        if not verse:
            return ""
        verse_map = {
            Verse.FPE: "Fonction publique d'État",
            Verse.FPH: "Fonction publique Hospitalière",
            Verse.FPT: "Fonction publique Territoriale",
        }
        return verse_map.get(verse, "")


class ConcoursToTemplateMapper(_BaseMapper):
    """Maps Concours entities to template-compatible dictionaries."""

    @staticmethod
    def map(concours: Concours) -> dict[str, str | list[str]]:
        """Transform a Concours entity to template format."""
        return {
            "opportunity_type": "concours",
            "title": concours.corps,
            "description": concours.grade,
            "access_modalities": [str(m) for m in concours.access_modality]
            if concours.access_modality
            else [],
            "category": ConcoursToTemplateMapper._format_category_display(
                concours.category
            ),
            "category_value": ConcoursToTemplateMapper._format_category_value(
                concours.category
            ),
            "versant": ConcoursToTemplateMapper._format_verse(Verse.FPE),
            "url": "#",
        }


class OfferToTemplateMapper(_BaseMapper):
    """Maps Offer entities to template-compatible dictionaries."""

    @staticmethod
    def map(offer: Offer) -> dict[str, str | list[str]]:
        """Transform an Offer entity to template format."""
        return {
            "opportunity_type": "offer",
            "title": offer.title,
            "description": offer.mission,
            "location": OfferToTemplateMapper._format_location_display(
                offer.localisation
            ),
            "category": OfferToTemplateMapper._format_category_display(offer.category),
            "versant": OfferToTemplateMapper._format_verse(offer.verse),
            "contract_type_display": OfferToTemplateMapper._format_contract_type(
                offer.contract_type
            ),
            "url": str(offer.offer_url) if offer.offer_url else "#",
        }

    @staticmethod
    def _format_location_display(localisation) -> str:
        """Format localisation for display."""
        if not localisation:
            return ""
        return f"{localisation.region}, {localisation.department}"

    @staticmethod
    def _format_contract_type(contract_type: ContractType | None) -> str:
        """Format contract type for display."""
        if not contract_type:
            return ""
        contract_map = {
            ContractType.TITULAIRE_CONTRACTUEL: "Titulaire / Contractuel",
            ContractType.CONTRACTUELS: "Contractuels",
            ContractType.TERRITORIAL: "Territorial",
        }
        return contract_map.get(contract_type, str(contract_type))
