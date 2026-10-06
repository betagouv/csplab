from referentiel.value_objects.category import Category
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.offer_nature import OfferNature
from referentiel.value_objects.verse import Verse

from domain.candidate.value_objects.opportunity_type import OpportunityType

CATEGORY_DISPLAY: dict[Category, str] = {
    Category.APLUS: "Catégorie A+",
    Category.A: "Catégorie A",
    Category.B: "Catégorie B",
    Category.C: "Catégorie C",
}

VERSE_DISPLAY: dict[Verse, str] = {
    Verse.FPE: "Fonction publique de l'État",
    Verse.FPT: "Fonction publique Territoriale",
    Verse.FPH: "Fonction publique Hospitalière",
}

OPPORTUNITY_TYPE_DISPLAY: dict[str, str] = {
    OpportunityType.OFFER: "Offre",
    OpportunityType.CONCOURS: "Concours",
}

OPPORTUNITY_TYPE_FILTER_DISPLAY: dict[OpportunityType, str] = {
    OpportunityType.OFFER: "Offre d'emploi",
    OpportunityType.CONCOURS: "Concours",
}


def format_category_display(category: Category | None) -> str:
    """Format category for display (e.g., 'Catégorie A')."""
    if not category:
        return ""
    return CATEGORY_DISPLAY.get(category, "")


def format_verse_display(verse: Verse | None) -> str:
    """Format verse for display (e.g., 'Fonction publique de l'État')."""
    if not verse:
        return ""
    return VERSE_DISPLAY.get(verse, "")


OFFER_NATURE_DISPLAY: dict[OfferNature, str] = {
    OfferNature.TITULAIRE_CONTRACTUEL: "Titulaire / Contractuel",
    OfferNature.CONTRACTUEL: "Contractuels",
    OfferNature.TERRITORIAL: "Territorial",
}


def format_offer_nature_display(offer_nature: OfferNature | None) -> str:
    """Format contract type for display."""
    if not offer_nature:
        return ""
    return OFFER_NATURE_DISPLAY.get(offer_nature, str(offer_nature))


def format_opportunity_type_display(opportunity_type: str | None) -> str:
    """Format opportunity type for display."""
    if not opportunity_type:
        return ""
    return OPPORTUNITY_TYPE_DISPLAY.get(opportunity_type, str(opportunity_type))


def format_location_display(localisation: Localisation | None) -> str:
    """Format localisation for display."""
    if not localisation:
        return ""
    return localisation.department.name
