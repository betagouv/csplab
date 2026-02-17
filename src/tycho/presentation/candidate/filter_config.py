"""Filter configuration for candidate search results."""

from domain.value_objects.category import Category
from domain.value_objects.verse import Verse
from presentation.candidate.formatters import (
    CATEGORY_DISPLAY,
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

OPPORTUNITY_TYPES: frozenset[str] = frozenset({"offer", "concours"})


def format_category_value(category: Category | None) -> str:
    """Format category value for filtering."""
    if not category:
        return ""
    return CATEGORY_FILTER_VALUE.get(category, "")


def get_category_filter_options() -> list[FilterOption]:
    """Build category filter options from domain enum."""
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
    """All possible category filter values (for 'select all' logic)."""
    return {
        v for cat, v in CATEGORY_FILTER_VALUE.items() if cat not in EXCLUDED_CATEGORIES
    }


def get_verse_filter_options() -> list[FilterOption]:
    """Build versant filter options from domain enum."""
    return [
        FilterOption(value=member.value, text=VERSE_DISPLAY[member]) for member in Verse
    ]


def get_verse_all_filter_values() -> set[str]:
    """All possible verse filter values (for 'select all' logic)."""
    return {member.value for member in Verse}
