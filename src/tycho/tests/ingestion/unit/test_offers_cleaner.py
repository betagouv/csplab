from unittest.mock import MagicMock

import pytest

from domain.value_objects.category import Category
from infrastructure.gateways.ingestion.offers_cleaner import OffersCleaner
from tests.utils.in_memory_offers_repository import InMemoryOffersRepository


@pytest.fixture
def offers_cleaner():
    return OffersCleaner(
        logger=MagicMock(),
        offers_repository=InMemoryOffersRepository(),
    )


class TestParseCategory:
    @pytest.mark.parametrize(
        "category_code",
        ["CAT-AEF", "CAT-ESD", "CAT-ES"],
    )
    def test_aplus_codes_return_aplus(self, offers_cleaner, category_code):
        assert offers_cleaner._parse_category(category_code) == Category.APLUS

    def test_cat_a_returns_a(self, offers_cleaner):
        assert offers_cleaner._parse_category("CAT-A") == Category.A

    def test_cat_b_returns_b(self, offers_cleaner):
        assert offers_cleaner._parse_category("CAT-B") == Category.B

    def test_cat_c_returns_c(self, offers_cleaner):
        assert offers_cleaner._parse_category("CAT-C") == Category.C

    def test_unknown_code_returns_none(self, offers_cleaner):
        assert offers_cleaner._parse_category("CAT-UNKNOWN") is None

    def test_none_returns_none(self, offers_cleaner):
        assert offers_cleaner._parse_category(None) is None
