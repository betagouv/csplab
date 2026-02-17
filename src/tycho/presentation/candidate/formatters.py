"""Shared presentation formatters for domain value objects."""

from domain.value_objects.category import Category
from domain.value_objects.contract_type import ContractType
from domain.value_objects.localisation import Localisation
from domain.value_objects.verse import Verse

CATEGORY_DISPLAY: dict[Category, str] = {
    Category.APLUS: "Catégorie A",
    Category.A: "Catégorie A",
    Category.B: "Catégorie B",
    Category.C: "Catégorie C",
}

VERSE_DISPLAY: dict[Verse, str] = {
    Verse.FPE: "Fonction publique d'État",
    Verse.FPT: "Fonction publique Territoriale",
    Verse.FPH: "Fonction publique Hospitalière",
}


def format_category_display(category: Category | None) -> str:
    """Format category for display (e.g., 'Catégorie A')."""
    if not category:
        return ""
    return CATEGORY_DISPLAY.get(category, "")


def format_verse_display(verse: Verse | None) -> str:
    """Format verse for display (e.g., 'Fonction publique d'État')."""
    if not verse:
        return ""
    return VERSE_DISPLAY.get(verse, "")


CONTRACT_TYPE_DISPLAY: dict[ContractType, str] = {
    ContractType.TITULAIRE_CONTRACTUEL: "Titulaire / Contractuel",
    ContractType.CONTRACTUELS: "Contractuels",
    ContractType.TERRITORIAL: "Territorial",
}


def format_contract_type_display(contract_type: ContractType | None) -> str:
    """Format contract type for display."""
    if not contract_type:
        return ""
    return CONTRACT_TYPE_DISPLAY.get(contract_type, str(contract_type))


def format_location_display(localisation: Localisation | None) -> str:
    """Format localisation for display."""
    if not localisation:
        return ""
    return localisation.department.name
