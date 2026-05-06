import pytest
from django.http import QueryDict

from domain.value_objects.category import Category
from presentation.candidate.filter_config import format_category_value
from presentation.candidate.formatters import format_category_display
from presentation.candidate.mappers import ViewFiltersToUsecaseMapper


@pytest.mark.parametrize(
    "category, expected",
    [
        (Category.APLUS, "Catégorie A+"),
        (Category.A, "Catégorie A"),
        (Category.B, "Catégorie B"),
        (Category.C, "Catégorie C"),
    ],
)
def test_format_category_display(category, expected):
    assert format_category_display(category) == expected


def test_aplus_and_a_have_distinct_display():
    assert format_category_display(Category.APLUS) != format_category_display(
        Category.A
    )


@pytest.mark.parametrize(
    "category, expected",
    [
        (Category.APLUS, "aplus"),
        (Category.A, "a"),
        (Category.B, "b"),
        (Category.C, "c"),
    ],
)
def test_format_category_value(category, expected):
    assert format_category_value(category) == expected


def test_aplus_and_a_have_distinct_filter_values():
    assert format_category_value(Category.APLUS) != format_category_value(Category.A)


def test_filter_param_aplus_maps_to_aplus_category():
    mapper = ViewFiltersToUsecaseMapper()
    filters = mapper.to_domain(QueryDict("filter-category=aplus"))
    assert filters["category"] == [Category.APLUS]


def test_filter_param_a_does_not_include_aplus_category():
    mapper = ViewFiltersToUsecaseMapper()
    filters = mapper.to_domain(QueryDict("filter-category=a"))
    assert Category.APLUS not in filters["category"]
