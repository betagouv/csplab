"""Filter configuration for candidate search results."""

from domain.value_objects.category import Category
from domain.value_objects.localisation import Localisation
from domain.value_objects.opportunity_type import OpportunityType
from domain.value_objects.verse import Verse
from presentation.candidate.formatters import (
    CATEGORY_DISPLAY,
    OPPORTUNITY_TYPE_FILTER_DISPLAY,
    VERSE_DISPLAY,
)
from presentation.candidate.types import FilterOption

EXCLUDED_CATEGORIES: frozenset[Category] = frozenset({Category.HORS_CATEGORIE})

CATEGORY_FILTER_VALUE: dict[Category, str] = {
    Category.APLUS: "a",
    Category.A: "a",
    Category.B: "b",
    Category.C: "c",
}

OPPORTUNITY_TYPES: frozenset[str] = frozenset(OpportunityType)


def get_opportunity_type_filter_options() -> list[FilterOption]:
    return [
        FilterOption(value=member.value, text=OPPORTUNITY_TYPE_FILTER_DISPLAY[member])
        for member in OpportunityType
    ]


def format_category_value(category: Category | None) -> str:
    if not category:
        return ""
    return CATEGORY_FILTER_VALUE.get(category, "")


def format_location_value(localisation: Localisation | None) -> str:
    if not localisation:
        return ""
    return str(localisation.department)


def get_category_filter_options() -> list[FilterOption]:
    seen: set[str] = set()
    options: list[FilterOption] = []
    for member in Category:
        if member in EXCLUDED_CATEGORIES:
            continue
        value = CATEGORY_FILTER_VALUE[member]
        if value in seen:
            continue
        seen.add(value)
        options.append(FilterOption(value=value, text=CATEGORY_DISPLAY[member]))
    return options


def get_category_all_filter_values() -> set[str]:
    return {
        v for cat, v in CATEGORY_FILTER_VALUE.items() if cat not in EXCLUDED_CATEGORIES
    }


def get_verse_filter_options() -> list[FilterOption]:
    return [
        FilterOption(value=member.value, text=VERSE_DISPLAY[member]) for member in Verse
    ]


def get_verse_all_filter_values() -> set[str]:
    return {member.value for member in Verse}


def get_location_filter_options(
    locations: list[tuple[str, str]],
) -> list[FilterOption]:
    options: list[FilterOption] = [
        FilterOption(value="", text="Toutes les localisations"),
    ]
    seen: set[str] = set()
    for value, display in locations:
        if not value or value in seen:
            continue
        seen.add(value)
        options.append(FilterOption(value=value, text=display))
    options[1:] = sorted(options[1:], key=lambda o: o["text"])
    return options
